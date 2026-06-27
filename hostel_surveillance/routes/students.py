import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, request, jsonify, session
from db.db_manager import DatabaseManager
from services.face_recognizer import FaceRecognizer
import routes.camera as camera_route
from functools import wraps

students_bp = Blueprint('students', __name__)
db = DatabaseManager()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@students_bp.route('/api/students', methods=['GET'])
@login_required
def get_students():
    students = db.fetch_all('SELECT * FROM students WHERE is_active=1')
    return jsonify([dict(s) for s in students])

@students_bp.route('/api/students', methods=['POST'])
@login_required
def add_student():
    data = request.get_json()
    try:
        sid = db.execute(
            'INSERT INTO students (roll_number, name, email, phone, room_number, hostel_block, course, year) VALUES (?,?,?,?,?,?,?,?)',
            (data['roll_number'], data['name'], data.get('email'), data.get('phone'),
             data.get('room_number'), data.get('hostel_block'), data.get('course'), data.get('year'))
        )
        return jsonify({'message': 'Student added', 'id': sid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@students_bp.route('/api/students/<int:sid>', methods=['PUT'])
@login_required
def update_student(sid):
    data = request.get_json()
    db.execute(
        'UPDATE students SET name=?, email=?, phone=?, room_number=?, hostel_block=?, course=?, year=? WHERE id=?',
        (data.get('name'), data.get('email'), data.get('phone'),
         data.get('room_number'), data.get('hostel_block'), data.get('course'), data.get('year'), sid)
    )
    return jsonify({'message': 'Student updated'})

@students_bp.route('/api/students/<int:sid>', methods=['DELETE'])
@login_required
def delete_student(sid):
    student = db.fetch_one('SELECT roll_number FROM students WHERE id=?', (sid,))
    if student:
        deleted_roll = f"{student['roll_number']}_deleted_{sid}"
        db.execute('UPDATE students SET is_active=0, roll_number=? WHERE id=?', (deleted_roll, sid))
    else:
        db.execute('UPDATE students SET is_active=0 WHERE id=?', (sid,))

    db.execute('DELETE FROM face_embeddings WHERE person_type=? AND person_id=?', ('student', sid))

    student_folder = os.path.join('data', 'known_faces', 'students', str(sid))
    if os.path.isdir(student_folder):
        try:
            for root, dirs, files in os.walk(student_folder, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(student_folder)
        except Exception:
            pass

    if camera_route.camera_service is not None:
        camera_route.camera_service.reload_embeddings()

    return jsonify({'message': 'Student removed'})


@students_bp.route('/api/students/delete_all', methods=['POST'])
@login_required
def delete_all_students():
    # Only allow admin to perform full truncate via UI
    if session.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    # Get all student ids
    rows = db.fetch_all('SELECT id FROM students')
    ids = [r['id'] for r in rows]

    # Delete embeddings and attendance records for each student
    for sid in ids:
        db.execute('DELETE FROM face_embeddings WHERE person_type=? AND person_id=?', ('student', sid))
        db.execute('DELETE FROM attendance_records WHERE student_id=?', (sid,))

        # Remove known_faces folder
        student_folder = os.path.join('data', 'known_faces', 'students', str(sid))
        if os.path.isdir(student_folder):
            try:
                for root, dirs, files in os.walk(student_folder, topdown=False):
                    for f in files:
                        os.remove(os.path.join(root, f))
                    for d in dirs:
                        os.rmdir(os.path.join(root, d))
                os.rmdir(student_folder)
            except Exception:
                pass

    # Finally remove student rows
    db.execute('DELETE FROM students')

    # Reload embeddings if camera running
    if camera_route.camera_service is not None:
        camera_route.camera_service.reload_embeddings()

    return jsonify({'message': 'All students removed'})

@students_bp.route('/api/students/<int:sid>/face', methods=['POST'])
@login_required
def upload_face(sid):
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    save_dir = f'data/known_faces/students/{sid}'
    os.makedirs(save_dir, exist_ok=True)
    path = f'{save_dir}/face.jpg'
    file.save(path)
    try:
        r = FaceRecognizer()
        db.execute('DELETE FROM face_embeddings WHERE person_type=? AND person_id=?', ('student', sid))
        r.add_face('student', sid, path)
        if camera_route.camera_service is not None:
            camera_route.camera_service.reload_embeddings()
        return jsonify({'message': 'Face registered successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
