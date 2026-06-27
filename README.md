# Hostel Surveillance System

A comprehensive real-time face recognition and attendance management system for hostel facilities. The system automatically detects, recognizes, and logs student presence using advanced deep learning models, with role-based access control and instant alert notifications for security breaches.

---

## 📋 Project Overview

The **Hostel Surveillance System** is a production-ready Flask web application that integrates computer vision and machine learning for automated hostel security and attendance tracking. It monitors live camera feeds, identifies registered students and blacklisted persons in real-time, logs recognition events with confidence scores, and sends alerts via email/SMS when unauthorized or unknown individuals are detected.

### Key Capabilities
- **Real-time Face Recognition**: Continuous live camera feed processing using ArcFace embeddings
- **Attendance Automation**: Automatic student presence marking with duplicate detection
- **Security Alerts**: Instant email/SMS notifications for blacklisted or unknown persons
- **Role-Based Access Control**: Separate dashboards and permissions for admins and wardens
- **Comprehensive Logging**: Detailed recognition logs, attendance records, and alert history
- **Student & Blacklist Management**: Full CRUD operations for student and restricted person databases

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0 (Python 3.10)
- **Database**: SQLite3 with relationship constraints
- **Face Recognition**: DeepFace 0.0.79 with ArcFace model
- **Computer Vision**: OpenCV 4.8.1.78
- **Authentication**: bcrypt for password hashing
- **Session Management**: Flask-Session
- **Notifications**: 
  - SMTP (Gmail) for email alerts
  - Twilio SDK for SMS (optional)
  - Email-to-SMS gateway support

### Frontend
- **Language**: HTML5 + Vanilla JavaScript (ES6+)
- **Styling**: Bootstrap 5.3 with custom CSS
- **Icons**: Font Awesome 6
- **Real-time Updates**: Fetch API with polling (logs update every 2 seconds)
- **Responsive Design**: Mobile-friendly dashboard with flexbox layout

### DevOps & Environment
- **Package Management**: pip
- **Virtual Environment**: venv
- **Environment Variables**: python-dotenv for secure credential storage
- **Testing**: pytest framework included

---

## 📁 Project Structure

```
hostel_surveillance/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration (DB path, model settings, email/SMS)
│
├── db/                             # Database layer
│   ├── __init__.py
│   ├── db_manager.py              # SQLite connection wrapper & query executor
│   ├── init_db.py                 # Database initialization & seeding script
│   ├── schema.sql                 # Database schema (11 tables)
│   └── hostel_copy.db             # SQLite database file
│
├── models/                         # Data models (reserved for ORM)
│   └── __init__.py
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── face_recognizer.py         # ArcFace embedding & matching (0.55 threshold)
│   ├── face_detector.py           # Cascade-based face detection
│   ├── camera_service.py          # Live camera capture (1 FPS, threading)
│   ├── attendance_service.py      # Attendance marking (30-min duplicate window)
│   ├── alert_service.py           # Email/SMS alerts (6-frame threshold for unknown)
│   └── [placeholder for other services]
│
├── routes/                         # API endpoints (blueprint-based)
│   ├── __init__.py
│   ├── auth.py                    # Login/logout, role-based auth
│   ├── students.py                # CRUD students, face upload, delete-all endpoint
│   ├── blacklist.py               # CRUD blacklisted persons
│   ├── attendance.py              # Attendance records & summary
│   ├── camera.py                  # Live stream, frame capture, status
│   ├── alerts.py                  # Alert history & acknowledgment
│   ├── dashboard.py               # Dashboard stats & summaries
│   ├── logs.py                    # Recognition logs (searchable, paginated)
│   └── [other route handlers]
│
├── static/                         # Frontend assets
│   ├── css/
│   │   └── style.css              # Custom styles (dark theme, responsive)
│   ├── img/                       # Logo & graphics
│   └── js/
│       └── app.js                 # Single-page app logic & API client
│
├── templates/                      # HTML templates
│   ├── base.html                  # Main SPA layout
│   ├── login.html                 # Authentication page
│   └── [other template stubs]
│
├── data/                           # Local storage
│   ├── known_faces/               # Registered face photos
│   │   └── students/{id}/         # Per-student folder
│   ├── unknown_captures/          # Unrecognized person frames
│   └── alert_frames/              # Blacklist alert snapshots
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_recognition.py        # Face recognition unit tests
│   └── [other test files]
│
├── docs/                           # Documentation (expandable)
│   └── [Architecture, API docs, etc.]
│
├── requirements.txt               # Python dependencies (11 packages)
├── .env.example                   # Environment variable template
└── README.md                       # This file

```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Windows/Linux/macOS with webcam support
- Gmail account with app-specific password (for email alerts)
- Twilio account (optional, for SMS)

### Step 1: Clone & Create Virtual Environment
```bash
cd "D:\BE Project\hostel_surveillance - Copy"
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# or: source venv/bin/activate  # Linux/macOS
```

### Step 2: Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
# Copy template
copy .env.example .env

# Edit .env with your credentials:
# SMTP_USER=your-email@gmail.com
# SMTP_PASS=your-app-password
# WARDEN_EMAIL=warden@example.com
# TWILIO_SID=your-twilio-sid (optional)
# TWILIO_TOKEN=your-twilio-token (optional)
# TWILIO_FROM=+1234567890 (optional)
# WARDEN_PHONE=+911234567890 (optional)
```

### Step 4: Initialize Database
```bash
cd hostel_surveillance
python db/init_db.py
# Output:
# ✅ Database initialized at: D:\...\hostel_surveillance\db\hostel_copy.db
#   - Admin user: admin / admin123
#   - Warden user: warden1 / warden123
#   - Sample staff record: EMP001 / Staff One
#   - Seeded student: CS001 / Student One
```

### Step 5: Run the Application
```bash
python app.py
# Output:
# [CameraService] Initialized.
# [CameraService] Camera started.
# * Running on http://127.0.0.1:5000
```

### Step 6: Access & Login
- Open browser: **http://127.0.0.1:5000**
- Login as **admin** (admin123) or **warden1** (warden123)
- Grant camera permission when prompted

---

## 📊 Database Schema

### Core Tables (SQLite)

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `students` | Registered hostel residents | id, roll_number (UNIQUE), name, email, phone, room_number, hostel_block, course, year, is_active |
| `admins` | System administrators | id, username (UNIQUE), password (bcrypt), email |
| `wardens` | Hostel wardens/supervisors | id, name, username (UNIQUE), password (bcrypt), email, phone, hostel_block, is_active |
| `staff` | Security/support staff | id, employee_id (UNIQUE), name, role, email, phone, is_active |
| `face_embeddings` | ArcFace embeddings (512-dim vectors) | id, person_type (student/blacklisted), person_id, image_path, embedding (BLOB), model_used |
| `attendance_records` | Marked attendance | id, student_id (FK), date, time_in, time_out, status, UNIQUE(student_id, date) |
| `recognition_logs` | All recognition events | id, timestamp, person_type, person_id, confidence, frame_path, camera_id |
| `alerts` | Security alerts | id, alert_type (blacklist/unknown), person_id, person_type, timestamp, image_path, email_sent, sms_sent, acknowledged |
| `blacklisted_persons` | Restricted/unauthorized persons | id, name, reason, added_by (FK warden), image_path |
| `attendance_summary` | Daily aggregate (derived) | date, total_present, total_absent |
| *Additional tables for extensions* | | |

### Key Constraints
- Foreign key relationships enforced (e.g., attendance.student_id → students.id)
- Soft deletes: students.is_active = 0 (rather than hard delete)
- Roll number uniqueness with rename-on-delete pattern to allow reuse

---

## 🎯 Core Features & Usage

### 1. **Dashboard**
- Real-time statistics: total students, present today, unacked alerts, recognition logs
- Recent recognition logs with confidence scores
- Daily attendance summary

### 2. **Live Camera Feed**
- Real-time MJPEG stream (1 FPS processing)
- Face detection boxes overlaid on video
- Live detections panel showing recognized persons with confidence % and timestamp
- Graceful retry on stream errors

### 3. **Student Management**
- **Add Student**: Roll number, name, email, phone, hostel block, course, year
- **Register Face**: Upload photo or capture from live camera
- **View All**: Active students with status and actions
- **Edit**: Update student details
- **Delete**: Soft-delete (marks is_active=0, renames roll for reuse)
- **Delete All**: Truncate all students (admin-only, resets DB for testing)

### 4. **Attendance Tracking**
- Automatic marking when registered student is recognized
- Duplicate prevention: 30-min window to prevent double-marking
- Time-in / time-out recording
- Daily & historical attendance reports
- Exportable logs

### 5. **Blacklist Management**
- Add restricted persons (e.g., trespassers, expelled students)
- Reason for restriction
- Snapshot image storage
- Real-time alert on detection

### 6. **Alert System**
- **Unknown Person Alert**: Triggered after 6 recognition frames (confidence < 0.55) within 12-sec window
- **Blacklist Alert**: Immediate notification with image
- Email alerts sent to configured warden email
- SMS alerts via Twilio or email-to-SMS gateway (optional)
- Acknowledgment tracking

### 7. **Recognition Logs**
- Searchable & filterable by person_type, confidence, date
- Paginated (15 logs per page, loads latest)
- Shows: person type, name/ID, confidence %, timestamp
- Useful for debugging false positives/negatives

### 8. **Role-Based Access Control**
- **Admin**: Full system access (students, camera, alerts, logs, blacklist, delete-all)
- **Warden**: Students, attendance, camera, alerts, logs (no student deletion)
- **Staff**: View-only mode (extensible in future)

---

## 🔧 Configuration & Performance Tuning

### `config.py` Settings

```python
# Face Recognition
FACE_MODEL = 'ArcFace'                    # Deep learning model
FACE_DETECTOR = 'opencv'                  # Cascade classifier (faster)
SIMILARITY_THRESHOLD = 0.55               # Cosine distance threshold (lower = stricter)
RECOGNITION_FPS = 2                       # Target FPS (actual: 1 FPS)

# Processing
DUPLICATE_WINDOW_MINUTES = 30             # Attendance duplicate window

# Alert Thresholds
unknown_threshold = 6                      # Frames before unknown alert
unknown_window = 12 seconds                # Window to accumulate frames

# Database
DATABASE_PATH = 'db/hostel_copy.db'       # SQLite file location

# File Paths
KNOWN_FACES_DIR = 'data/known_faces'      # Registered face storage
UNKNOWN_CAPTURES = 'data/unknown_captures' # Unknown person frames
ALERT_FRAMES_DIR = 'data/alert_frames'    # Alert snapshots
```

### Performance Optimizations Implemented
1. **Frame Processing**: 1 FPS polling (vs. real-time) to reduce CPU load
2. **Largest Face Priority**: Process largest detected face per frame (ignore small faces in background)
3. **Embedding Caching**: All embeddings loaded into memory at startup
4. **Cascade Detector**: Fast OpenCV Cascade instead of heavy MTCNN
5. **Image Resizing**: Downscale large frames to 224px before embedding
6. **Thread Safety**: Thread locks for frame access to prevent race conditions
7. **Graceful Degradation**: Try/except blocks prevent single error from breaking stream
8. **DB Connection Pooling**: Reuse SQLite connections (implicit in sqlite3)

### For Heavy Load (Many Students/Cameras)
- Move face recognition to multiprocessing (separate worker)
- Use PostgreSQL instead of SQLite
- Add Redis for session caching
- Scale to multiple camera streams

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` — Login (returns role)
- `POST /api/auth/logout` — Logout
- `GET /api/auth/me` — Get current user

### Students
- `GET /api/students` — List active students
- `POST /api/students` — Add student
- `PUT /api/students/<id>` — Update student
- `DELETE /api/students/<id>` — Soft-delete student
- `POST /api/students/<id>/face` — Register face image
- `POST /api/students/delete_all` — Truncate all students (admin-only)

### Attendance
- `GET /api/attendance?date=YYYY-MM-DD` — Daily attendance
- `GET /api/attendance/all?limit=100` — Recent attendance records

### Camera
- `GET /api/camera/stream` — MJPEG live feed
- `GET /api/camera/capture` — Single frame snapshot
- `GET /api/camera/status` — Camera running status

### Alerts
- `GET /api/alerts` — Alert history
- `PUT /api/alerts/<id>` — Acknowledge alert

### Logs
- `GET /api/logs?limit=15` — Recent recognition logs
- `GET /api/logs?person_type=student&date=YYYY-MM-DD` — Filtered logs

### Blacklist
- `GET /api/blacklist` — List restricted persons
- `POST /api/blacklist` — Add to blacklist
- `DELETE /api/blacklist/<id>` — Remove from blacklist
- `POST /api/blacklist/<id>/face` — Register blacklist face

### Dashboard
- `GET /api/dashboard` — Stats (total students, present today, alerts, logs count)

---

## 🎓 Technical Highlights for Resume

### Skills Demonstrated
- **Backend Development**: Flask, RESTful API design, session management, bcrypt authentication
- **Database Design**: SQLite schema with foreign keys, transactions, soft deletes, UNIQUE constraints
- **Computer Vision**: OpenCV face detection (Cascade Classifier), multi-face handling
- **Deep Learning**: DeepFace library, ArcFace embeddings, cosine similarity matching, threshold tuning
- **Real-time Processing**: Multi-threading, thread safety (locks), continuous capture loops
- **Frontend Development**: Vanilla JavaScript (no frameworks), DOM manipulation, responsive Bootstrap UI, single-page app (SPA) architecture
- **DevOps**: Virtual environments, environment variable management, error handling & logging
- **Email/SMS Integration**: SMTP, Twilio API, email-to-SMS gateways
- **Testing & Debugging**: pytest, logging, exception handling, edge case management

### Production-Ready Features
- Role-based access control (RBAC) with session validation
- Error recovery (graceful degradation in camera stream, try/except in critical paths)
- Data validation (UNIQUE constraints, relationship integrity)
- Scalability hooks (thread-safe design, configurable thresholds, extensible route structure)
- Security: bcrypt password hashing, SQL injection prevention (parameterized queries), CSRF protection potential
- Performance: 1 FPS processing, image resizing, embedding caching, efficient face detection

### Code Quality
- Clear separation of concerns (services, routes, static)
- Comprehensive logging throughout
- Consistent naming conventions
- Modular route handlers
- Documented configuration

---

## 📈 Usage Scenarios

### Scenario 1: Daily Attendance Tracking
1. Admin registers all 100 students with photos
2. System runs continuously; students enter hostel
3. Camera recognizes and auto-marks attendance
4. Warden reviews daily attendance report

### Scenario 2: Security Breach Detection
1. Unknown person detected → system logs 6+ frames
2. Email alert sent to warden with snapshot
3. Warden can acknowledge alert or investigate
4. All logs viewable in recognition history

### Scenario 3: Blacklist Enforcement
1. Admin adds expelled student to blacklist
2. If that student tries to enter, immediate alert sent
3. Security can respond in real-time

### Scenario 4: Testing & Iteration
1. Admin clicks "Delete All Students" to reset
2. Adds new students with different photos
3. Tests recognition accuracy at different thresholds
4. Tuning SIMILARITY_THRESHOLD for environment-specific lighting/angles

---

## 🔒 Security Considerations

- **Password Storage**: bcrypt with salt (never plaintext)
- **Session Management**: Flask-Session with secure cookies
- **Database**: SQLite with PRAGMA foreign_keys enforced
- **Input Validation**: Parameterized SQL queries (no string concatenation)
- **File Upload**: Images saved to isolated `data/` directory
- **Role Enforcement**: API endpoints check `session['role']` before returning data
- **Environment Secrets**: Credentials in `.env`, not in code

---

## 🚨 Known Limitations & Future Enhancements

### Current Limitations
- Single camera support (extensible to multiple via camera_id field)
- SQLite (not suitable for 100k+ students; upgrade to PostgreSQL for scale)
- Vanilla JS (no real-time WebSocket; uses polling for logs)
- No user signup (manual admin creation only)
- Staff role defined in DB but no dedicated UI login

### Future Enhancements
1. **Multi-Camera Support**: Add camera_id to recognition logs, support multiple concurrent streams
2. **Advanced Analytics**: Heatmaps, peak hours, suspicious patterns
3. **Scheduled Reports**: Auto-email daily/weekly summaries
4. **Mobile App**: React Native or Flutter frontend
5. **WebSocket Live Updates**: Real-time log streaming without polling
6. **Face Quality Metrics**: Reject blurry/low-res captures
7. **Liveness Detection**: Prevent spoofing with photos/videos
8. **Cloud Backup**: Auto-backup database to S3/Azure
9. **Two-Factor Auth**: SMS or TOTP for admin login
10. **Audit Logging**: Track all DB modifications with user/timestamp

---

## 📝 License & Attribution

This project uses:
- **DeepFace** (MIT License): https://github.com/serengil/deepface
- **OpenCV** (BSD License): https://opencv.org/
- **Flask** (BSD License): https://flask.palletsprojects.com/
- **Bootstrap** (MIT License): https://getbootstrap.com/

---

## 📞 Support & Troubleshooting

### Common Issues

#### **Camera feed turns black after 2–4 seconds**
- Check app terminal for `[CameraService]` or `[Camera Route]` errors
- Verify camera is not in use by another application
- Try unplugging and replugging camera
- Reduce image resolution in `camera_service.py` line 33–34 (CAP_PROP_FRAME_WIDTH/HEIGHT)

#### **Face recognition not working**
- Ensure face is at least 80×80 pixels (minSize in detectMultiScale)
- Check photo lighting and angle (ArcFace prefers frontal faces)
- Lower SIMILARITY_THRESHOLD in `config.py` if too many false negatives
- Review [FaceRecognizer.recognize()](services/face_recognizer.py) for confidence scores in logs

#### **Unknown person alerts too frequent**
- Increase `unknown_threshold` in `alert_service.py` (current: 6 frames)
- Adjust `unknown_window` to longer (current: 12 seconds)

#### **Email alerts not sending**
- Verify `.env` has correct SMTP_USER & SMTP_PASS (Gmail app password, not regular password)
- Check firewall/antivirus blocks SMTP port 587
- Review app terminal logs for `[Alert] Email failed: ...`

---

## 📚 Learning Resources

- **Face Recognition**: https://en.wikipedia.org/wiki/Facial_recognition_system
- **ArcFace**: https://arxiv.org/abs/1801.07698
- **Flask**: https://flask.palletsprojects.com/
- **OpenCV**: https://docs.opencv.org/
- **SQLite**: https://www.sqlite.org/docs.html

---

## ✨ Summary for Resume

**Hostel Surveillance System** is a full-stack Flask + Deep Learning project that integrates real-time computer vision (face detection & recognition) with a web application for attendance automation and security monitoring. The system demonstrates competency in backend API development, database design, computer vision integration, frontend development, and production-ready error handling. Suitable for portfolio showcase or as a reference for similar projects (campus security, airport screening, smart building access control).

**Tech Stack**: Python 3.10, Flask 3.0, SQLite3, DeepFace (ArcFace), OpenCV 4.8, Bootstrap 5, JavaScript (ES6+), bcrypt, SMTP/Twilio.

**Key Features**: Real-time face recognition, automatic attendance marking, role-based access control, email/SMS alerts, comprehensive logging, scalable architecture.

---

*Last Updated: June 27, 2026*  
*Version: 1.0 (Copy Project)*
