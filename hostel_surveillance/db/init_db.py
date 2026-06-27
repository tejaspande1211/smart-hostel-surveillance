import sqlite3
import os
import sys
import bcrypt
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE_PATH

def init_db():
    db_path = os.path.abspath(DATABASE_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()

    conn = sqlite3.connect(db_path)
    conn.executescript(schema)

    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn.execute(
        'INSERT INTO admins (username, password, email) VALUES (?,?,?)',
        ('admin', admin_password, 'admin@example.com')
    )
    warden_password = bcrypt.hashpw('warden123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn.execute(
        'INSERT INTO wardens (name, username, password, email, phone, hostel_block) VALUES (?,?,?,?,?,?)',
        ('Warden One', 'warden1', warden_password, 'warden1@example.com', '+911234567890', 'A')
    )
    conn.execute(
        'INSERT INTO staff (employee_id, name, role, email, phone) VALUES (?,?,?,?,?)',
        ('EMP001', 'Staff One', 'Security', 'staff1@example.com', '+911112223333')
    )
    conn.execute(
        'INSERT INTO students (roll_number, name, email, phone, room_number, hostel_block, course, year) VALUES (?,?,?,?,?,?,?,?)',
        ('CS001', 'Student One', 'cs001@example.com', '+911234567890', '101', 'A', 'B.Tech CS', 1)
    )

    conn.commit()
    conn.close()

    data_root = os.path.join(os.path.dirname(__file__), '..', 'data')
    for subdir in ['known_faces/students', 'unknown_captures', 'alert_frames']:
        Path(os.path.join(data_root, subdir)).mkdir(parents=True, exist_ok=True)

    print(f"✅ Database initialized at: {db_path}")
    print('  - Admin user: admin / admin123')
    print('  - Warden user: warden1 / warden123')
    print('  - Sample staff record: EMP001 / Staff One (staff login not implemented)')
    print('  - Seeded student: CS001 / Student One')

if __name__ == '__main__':
    init_db()