import os

BASE_DIR = os.path.dirname(__file__)

# Database
DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'db', 'hostel_copy.db'))

# Face Recognition
FACE_MODEL = 'ArcFace'
FACE_DETECTOR = 'opencv'          # opencv (not mtcnn) — avoids keras conflict
SIMILARITY_THRESHOLD = 0.55
RECOGNITION_FPS = 2

# File Paths
KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'data', 'known_faces')
UNKNOWN_CAPTURES = os.path.join(BASE_DIR, 'data', 'unknown_captures')
ALERT_FRAMES_DIR = os.path.join(BASE_DIR, 'data', 'alert_frames')

# Attendance
DUPLICATE_WINDOW_MINUTES = 30

# SMTP Email (Required for alerts)
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.environ.get('SMTP_USER')  # Gmail address
SMTP_PASS = os.environ.get('SMTP_PASS')  # Gmail App Password (NOT regular password)
WARDEN_EMAIL = os.environ.get('WARDEN_EMAIL')  # Warden's email

# Twilio SMS (Optional - either use Twilio OR SMS Gateway, not both)
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_FROM = os.environ.get('TWILIO_FROM')  # Twilio phone number
WARDEN_PHONE = os.environ.get('WARDEN_PHONE')  # Warden's phone (with country code: +91XXXXXXXXXX)
SMS_GATEWAY_DOMAIN = os.environ.get('SMS_GATEWAY_DOMAIN')  # Alternative: email-to-SMS gateway

