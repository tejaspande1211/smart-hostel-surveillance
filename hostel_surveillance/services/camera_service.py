import cv2
import threading
import time
from time_utils import now_ist
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.face_recognizer import FaceRecognizer
from db.db_manager import DatabaseManager
from services.alert_service import AlertService
from services.attendance_service import AttendanceService

class CameraService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.frame = None
        self.lock = threading.Lock()
        self.recognizer = FaceRecognizer()
        self.db = DatabaseManager()
        self.alert_svc = AlertService()
        self.attendance_svc = AttendanceService()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.last_recognition = {}
        print('[CameraService] Initialized.')

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not self.cap.isOpened():
            print('[CameraService] ERROR: Cannot open camera.')
            return False
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print('[CameraService] Camera started.')
        return True

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        print('[CameraService] Camera stopped.')

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def get_annotated_frame(self):
        """Returns frame with face boxes drawn — for live stream."""
        try:
            frame = self.get_frame()
            if frame is None:
                return None
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            return frame
        except Exception as e:
            print(f'[CameraService] get_annotated_frame error: {e}')
            return self.get_frame()

    def reload_embeddings(self):
        self.recognizer.load_embeddings_from_db()
        print('[CameraService] Embeddings reloaded')

    def _capture_loop(self):
        last_process_time = 0
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print('[CameraService] Frame read failed.')
                    time.sleep(0.1)
                    continue

                with self.lock:
                    self.frame = frame

                # Process only 1 FPS to reduce CPU load and avoid lag when multiple faces appear
                now = time.time()
                if now - last_process_time >= 1.0:
                    try:
                        self._process_frame(frame)
                    except Exception as e:
                        print(f'[CameraService] Error processing frame: {e}')
                    last_process_time = now
            except Exception as e:
                print(f'[CameraService] Capture loop exception: {e}')
                time.sleep(0.5)

    def _process_frame(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
            )
            if len(faces) == 0:
                return

            x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
            face_img = frame[y:y+h, x:x+w]
            result = self.recognizer.recognize(face_img)
            self._handle_recognition(result)
        except Exception as e:
            print(f'[CameraService] _process_frame error: {e}')

    def _handle_recognition(self, result):
        ptype = result['person_type']
        pid = result['person_id']
        conf = result['confidence']

        # Log every event
        self.db.execute(
            'INSERT INTO recognition_logs (person_type, person_id, confidence, timestamp) VALUES (?,?,?,?)',
            (ptype, pid, conf, now_ist().strftime('%Y-%m-%d %H:%M:%S'))
        )
        print(f'[Recognition] type={ptype} id={pid} confidence={conf}')

        # Route to correct service
        if ptype == 'student':
            student = self.db.fetch_one('SELECT * FROM students WHERE id=? AND is_active=1', (pid,))
            if student:
                self.attendance_svc.mark_attendance(pid)
            else:
                print(f'[Recognition] student id={pid} not active or not found, skipping attendance')
        elif ptype == 'blacklisted':
            person = self.db.fetch_one('SELECT * FROM blacklisted_persons WHERE id=?', (pid,))
            if person:
                frame = self.get_frame()
                if frame is not None:
                    self.alert_svc.send_blacklist_alert(pid, frame)
            else:
                print(f'[Recognition] blacklisted id={pid} not found; ignoring')
        elif ptype == 'unknown':
            frame = self.get_frame()
            if frame is not None:
                self.alert_svc.log_unknown(frame)