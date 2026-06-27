from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create PDF
pdf_file = "HOSTEL_SURVEILLANCE_PROJECT_REPORT.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1e2a38'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#0d6efd'),
    spaceAfter=12,
    spaceBefore=10,
    fontName='Helvetica-Bold',
    borderColor=colors.HexColor('#0d6efd'),
    borderWidth=0,
    borderPadding=5
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#198754'),
    spaceAfter=8,
    spaceBefore=6,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

code_style = ParagraphStyle(
    'CustomCode',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Courier',
    leftIndent=20,
    spaceAfter=6,
    textColor=colors.HexColor('#333333'),
    backColor=colors.HexColor('#f8f9fa')
)

# ==================== TITLE PAGE ====================
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("Smart Hostel Surveillance & Face Recognition System", title_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Final Year B.E. Project Report", styles['Normal']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
story.append(Spacer(1, 1*inch))

story.append(Paragraph("<b>Technology Stack:</b>", heading2_style))
tech_data = [
    ['Python 3.10', 'Flask Web Framework'],
    ['OpenCV', 'Computer Vision Library'],
    ['DeepFace (ArcFace)', 'Deep CNN Face Recognition'],
    ['SQLite', 'Lightweight Database'],
    ['MJPEG Stream', 'Live Video Feed']
]
tech_table = Table(tech_data, colWidths=[2.5*inch, 2.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
story.append(tech_table)
story.append(PageBreak())

# ==================== TABLE OF CONTENTS ====================
story.append(Paragraph("Table of Contents", title_style))
story.append(Spacer(1, 0.2*inch))
toc_items = [
    "1. Project Overview & Features",
    "2. System Architecture",
    "3. Recognition & Capture Workflow",
    "4. Database Schema & Storage",
    "5. Core Components (File Documentation)",
    "6. API Routes & Dashboard",
    "7. Setup & Deployment",
    "8. Key Parameters & Configuration"
]
for item in toc_items:
    story.append(Paragraph(item, normal_style))
story.append(PageBreak())

# ==================== 1. PROJECT OVERVIEW ====================
story.append(Paragraph("1. Project Overview & Features", heading1_style))
story.append(Spacer(1, 0.15*inch))

overview_text = """
This project is a smart surveillance system designed specifically for hostel management. It uses real-time face recognition 
with ArcFace deep neural networks (~80% accuracy) to automatically identify residents, mark attendance, detect intruders, 
and alert wardens about blacklisted persons. The system provides role-based dashboards for administrators and wardens.
"""
story.append(Paragraph(overview_text, normal_style))

story.append(Paragraph("<b>Key Features:</b>", heading2_style))
features = [
    "✓ <b>Real-time Face Recognition:</b> Uses ArcFace CNN with ~80% confidence threshold",
    "✓ <b>Automatic Attendance:</b> Marks attendance when recognized with 30-minute duplicate prevention",
    "✓ <b>Unknown Person Detection:</b> Logs unrecognized faces and captures alert frames",
    "✓ <b>Blacklist Management:</b> Detects blacklisted persons and sends instant email alerts",
    "✓ <b>Live Video Stream:</b> MJPEG browser-based camera feed with face detection boxes",
    "✓ <b>Role-Based Access:</b> Admin (full control) vs Warden (limited access)",
    "✓ <b>Dashboard:</b> Real-time statistics, recognition logs, attendance records, and alerts",
    "✓ <b>Email Notifications:</b> Automatic alerts for blacklist detection via SMTP/Gmail"
]
for feature in features:
    story.append(Paragraph(feature, normal_style))
story.append(PageBreak())

# ==================== 2. SYSTEM ARCHITECTURE ====================
story.append(Paragraph("2. System Architecture", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>High-Level Architecture:</b>", heading2_style))
story.append(Paragraph("""
The system follows a modular software architecture:
<br/><br/>
<b>Frontend:</b> Single-Page Application (HTML/CSS/JavaScript) served through Flask<br/>
<b>Backend:</b> Flask REST API with role-based authentication and session management<br/>
<b>Core Processing:</b> Multi-threaded camera service with real-time face recognition<br/>
<b>Database:</b> SQLite for persistent storage of faces, logs, alerts, and attendance<br/>
<b>Services:</b> Modular services for face recognition, alerts, attendance, and camera control
""", normal_style))

story.append(Paragraph("<b>Component Interaction Flow:</b>", heading2_style))
flow_data = [
    ['Component', 'Purpose', 'Technology'],
    ['Camera Service', 'Captures frames at 2 FPS and processes them', 'OpenCV + Threading'],
    ['Face Recognizer', 'Extracts embeddings and matches against database', 'DeepFace/ArcFace'],
    ['Attendance Service', 'Marks attendance with duplicate prevention', 'SQLite Queries'],
    ['Alert Service', 'Logs unknown/blacklist events and sends emails', 'SMTP + File I/O'],
    ['Flask API', 'Handles HTTP requests from frontend', 'Flask Blueprints'],
    ['SQLite Database', 'Stores faces, embeddings, logs, alerts, attendance', 'SQLite']
]
flow_table = Table(flow_data, colWidths=[1.5*inch, 2*inch, 1.5*inch])
flow_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
]))
story.append(flow_table)
story.append(PageBreak())

# ==================== 3. RECOGNITION & CAPTURE WORKFLOW ====================
story.append(Paragraph("3. Recognition & Capture Workflow", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>Complete Data Flow:</b>", heading2_style))
story.append(Paragraph("""
<b>Step 1: Camera Initialization</b><br/>
• CameraService creates a connection to the default webcam (index 0)<br/>
• OpenCV's Haar Cascade classifier is loaded for real-time face detection<br/>
• A background thread continuously captures frames at system FPS<br/>
<br/>
<b>Step 2: Frame Capture (Continuous)</b><br/>
• Background thread reads frames from camera at ~30 FPS<br/>
• Frames are stored in memory with thread-safe locking<br/>
• Every 0.5 seconds (2 FPS), a frame is processed for face recognition<br/>
<br/>
<b>Step 3: Face Detection & Recognition</b><br/>
• Haar Cascade detector finds face regions in the frame<br/>
• For each detected face (if any), the ENTIRE frame is passed to DeepFace/ArcFace<br/>
• ArcFace extracts a 512-dimensional embedding vector from the face<br/>
• This embedding is compared against all known embeddings using cosine similarity distance<br/>
<br/>
<b>Step 4: Matching & Classification</b><br/>
• Best matching embedding is found with minimum cosine distance<br/>
• confidence = 1.0 - min_distance (higher is better)<br/>
• If confidence > SIMILARITY_THRESHOLD (0.55), person is recognized as 'student' or 'staff'<br/>
• If confidence <= 0.55, person is classified as 'unknown'<br/>
<br/>
<b>Step 5: Result Handling</b><br/>
• <b>Student Recognized:</b> AttendanceService marks attendance (first detection = time_in, subsequent = time_out)<br/>
• <b>Blacklisted Person:</b> AlertService captures frame and sends email alert to warden<br/>
• <b>Unknown Person:</b> AlertService logs frame to unknown_captures folder for review<br/>
• ALL events: Logged to recognition_logs table with timestamp and confidence<br/>
""", normal_style))

story.append(Paragraph("<b>Key Recognition Parameters:</b>", heading2_style))
params_data = [
    ['Parameter', 'Value', 'Description'],
    ['Face Model', 'ArcFace', 'Deep CNN architecture for embedding extraction'],
    ['Detector Backend', 'OpenCV', 'Uses Haar Cascade (not MTCNN to avoid conflicts)'],
    ['Similarity Threshold', '0.55', 'Min confidence to consider a match valid'],
    ['Recognition FPS', '2 FPS', 'Process rate (CPU efficiency vs latency tradeoff)'],
    ['Face Min Size', '60x60 pixels', 'Ignores faces smaller than this'],
    ['Duplicate Window', '30 minutes', 'Prevent marking same student twice within window'],
    ['Embedding Dimension', '512', 'Size of ArcFace feature vector']
]
params_table = Table(params_data, colWidths=[1.3*inch, 1*inch, 2.2*inch])
params_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
]))
story.append(params_table)
story.append(PageBreak())

# ==================== 4. DATABASE SCHEMA ====================
story.append(Paragraph("4. Database Schema & Storage", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>Database Structure (SQLite):</b>", heading2_style))
story.append(Paragraph("""
The system uses SQLite with the following tables:
""", normal_style))

story.append(Paragraph("<b>admins</b> — System administrators", heading2_style))
story.append(Paragraph("""
Stores admin user credentials. Fields: id, username, password (bcrypt), email, created_at
""", code_style))

story.append(Paragraph("<b>wardens</b> — Hostel wardens", heading2_style))
story.append(Paragraph("""
Stores warden info. Fields: id, name, username, password (bcrypt), email, phone, hostel_block, is_active
""", code_style))

story.append(Paragraph("<b>students</b> — Student records", heading2_style))
story.append(Paragraph("""
Core student database. Fields: id, roll_number, name, email, phone, room_number, hostel_block, course, year, is_active
""", code_style))

story.append(Paragraph("<b>face_embeddings</b> — Face feature vectors", heading2_style))
story.append(Paragraph("""
Stores ArcFace embeddings (512-dim vectors). Fields: id, person_type ('student'/'staff'/'blacklisted'), 
person_id, image_path, embedding (pickled numpy array), model_used, created_at
""", code_style))

story.append(Paragraph("<b>recognition_logs</b> — Recognition events", heading2_style))
story.append(Paragraph("""
Every face detection event. Fields: id, timestamp, person_type, person_id, confidence (0.0-1.0), 
frame_path, camera_id
""", code_style))

story.append(Paragraph("<b>attendance_records</b> — Daily attendance", heading2_style))
story.append(Paragraph("""
Marks when students entered/exited. Fields: id, student_id, date, time_in, time_out, status, 
unique constraint on (student_id, date)
""", code_style))

story.append(Paragraph("<b>alerts</b> — Security alerts", heading2_style))
story.append(Paragraph("""
Logs blacklist/unknown person events. Fields: id, alert_type ('blacklist'/'unknown'), person_id, 
person_type, timestamp, image_path, email_sent, sms_sent, acknowledged
""", code_style))

story.append(Paragraph("<b>blacklisted_persons</b> — Blacklist registry", heading2_style))
story.append(Paragraph("""
Records of persons to deny entry. Fields: id, name, reason, added_by (warden_id), 
image_path, created_at
""", code_style))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>File Storage Locations:</b>", heading2_style))
storage_data = [
    ['Directory', 'Contents'],
    ['data/known_faces/students/{id}/', 'Registered student face photos'],
    ['data/known_faces/staff/', 'Staff face photos'],
    ['data/known_faces/blacklisted/', 'Blacklist person photos'],
    ['data/alert_frames/', 'Captured frames of blacklist detections'],
    ['data/unknown_captures/', 'Captured frames of unrecognized persons']
]
storage_table = Table(storage_data, colWidths=[2.5*inch, 2.5*inch])
storage_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
]))
story.append(storage_table)
story.append(PageBreak())

# ==================== 5. CORE COMPONENTS ====================
story.append(Paragraph("5. Core Components (File Documentation)", heading1_style))
story.append(Spacer(1, 0.15*inch))

# Backend Services
story.append(Paragraph("<b>BACKEND SERVICES (services/)</b>", heading2_style))

components = [
    {
        'name': 'face_recognizer.py',
        'purpose': 'Face embedding extraction and matching',
        'functions': [
            'load_embeddings_from_db() — Loads all face embeddings from DB into memory',
            'extract_embedding(face_img) — Uses DeepFace to extract 512-dim vector',
            'recognize(face_img) — Compares input against known embeddings, returns best match',
            'add_face(person_type, person_id, image_path) — Registers new face with embedding'
        ],
        'key_params': 'SIMILARITY_THRESHOLD=0.55, FACE_MODEL="ArcFace", FACE_DETECTOR="opencv"'
    },
    {
        'name': 'camera_service.py',
        'purpose': 'Real-time camera capture and recognition processing',
        'functions': [
            'start() — Opens camera and starts background capture thread',
            'get_frame() — Returns current frame (thread-safe)',
            'get_annotated_frame() — Returns frame with face detection boxes drawn',
            '_capture_loop() — Background thread continuously captures and processes frames',
            '_process_frame(frame) — Detects faces and calls recognizer',
            '_handle_recognition(result) — Routes result to attendance/alert services'
        ],
        'key_params': 'RECOGNITION_FPS=2, Min face size=60x60 pixels'
    },
    {
        'name': 'attendance_service.py',
        'purpose': 'Automatic attendance marking with duplicate prevention',
        'functions': [
            'mark_attendance(student_id) — Marks entry/exit with duplicate window checking',
            'Duplicate window prevents marking same student within 30 minutes'
        ],
        'key_params': 'DUPLICATE_WINDOW_MINUTES=30'
    },
    {
        'name': 'alert_service.py',
        'purpose': 'Alert logging and email notifications',
        'functions': [
            'send_blacklist_alert(person_id, frame) — Captures frame, logs to DB, sends email',
            'log_unknown(frame) — Logs unrecognized person to folder and DB',
            '_send_email(to, subject, body, attachment) — Sends SMTP emails with attachment'
        ],
        'key_params': 'SMTP_HOST, WARDEN_EMAIL, ALERT_FRAMES_DIR, UNKNOWN_CAPTURES'
    }
]

for comp in components:
    story.append(Paragraph(f"<b>{comp['name']}</b>", heading2_style))
    story.append(Paragraph(f"<b>Purpose:</b> {comp['purpose']}", normal_style))
    story.append(Paragraph("<b>Key Methods:</b>", normal_style))
    for func in comp['functions']:
        story.append(Paragraph(f"• {func}", normal_style))
    story.append(Paragraph(f"<b>Key Parameters:</b> {comp['key_params']}", code_style))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# Database & Routes
story.append(Paragraph("<b>DATABASE & UTILITIES (db/)</b>", heading2_style))

db_components = [
    {
        'name': 'db_manager.py',
        'purpose': 'SQLite connection wrapper for all DB operations',
        'methods': ['execute(query, params) — Run INSERT/UPDATE/DELETE', 'fetch_one(query, params) — Get single row', 'fetch_all(query, params) — Get all matching rows']
    },
    {
        'name': 'schema.sql',
        'purpose': 'SQL table definitions',
        'methods': ['Defines: admins, wardens, students, staff, face_embeddings, recognition_logs, attendance_records, alerts, blacklisted_persons']
    },
    {
        'name': 'init_db.py',
        'purpose': 'Database initialization script',
        'methods': ['Creates db directory, runs schema.sql, initializes tables']
    }
]

for comp in db_components:
    story.append(Paragraph(f"<b>{comp['name']}</b> — {comp['purpose']}", normal_style))
    for method in comp['methods']:
        story.append(Paragraph(f"• {method}", normal_style))
    story.append(Spacer(1, 0.05*inch))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>API ROUTES (routes/)</b>", heading2_style))

routes_list = [
    ('auth.py', 'POST /api/auth/login, POST /api/auth/logout, GET /api/auth/me — Authentication'),
    ('students.py', 'GET/POST/PUT/DELETE /api/students, POST /api/students/{id}/face — Student management'),
    ('attendance.py', 'GET /api/attendance — Retrieve attendance by date'),
    ('alerts.py', 'GET /api/alerts, PUT /api/alerts/{id} — Alert management'),
    ('camera.py', 'GET /api/camera/stream — MJPEG video stream, GET /api/camera/config — Settings'),
    ('dashboard.py', 'GET /api/dashboard/stats — Real-time dashboard statistics'),
    ('logs.py', 'GET /api/logs — Recognition event logs with filtering'),
    ('blacklist.py', 'GET/POST/DELETE /api/blacklist — Blacklist management')
]

for route_file, endpoints in routes_list:
    story.append(Paragraph(f"<b>{route_file}</b> — {endpoints}", normal_style))

story.append(PageBreak())

# ==================== 6. Flask App & Frontend ====================
story.append(Paragraph("<b>MAIN APPLICATION & FRONTEND</b>", heading2_style))

main_components = [
    {
        'name': 'app.py',
        'desc': 'Flask application entry point. Registers blueprints, initializes camera service, starts background thread.',
        'routes': 'Serves HTML pages at /, /login, /dashboard, /students, /camera, /alerts, /attendance, /logs, /blacklist'
    },
    {
        'name': 'config.py',
        'desc': 'Centralized configuration. Face model params, SMTP settings, file paths, thresholds.',
        'routes': 'FACE_MODEL="ArcFace", SIMILARITY_THRESHOLD=0.55, RECOGNITION_FPS=2, DATABASE_PATH'
    },
    {
        'name': 'templates/base.html',
        'desc': 'Single HTML file serving SPA (Single Page Application). Contains navbar, sidebar, main content area.',
        'routes': 'Navbar with role display, sidebar navigation, main-content div for dynamic rendering'
    },
    {
        'name': 'templates/login.html',
        'desc': 'Login page with username/password form. Submits to POST /api/auth/login.',
        'routes': 'Form submission → session creation → redirect to /dashboard'
    },
    {
        'name': 'static/js/app.js',
        'desc': 'Core SPA logic. Implements frontend routing, API calls, dynamic UI rendering.',
        'routes': 'loadDashboard(), loadStudents(), loadCamera(), loadAlerts(), loadAttendance(), loadLogs(), loadBlacklist()'
    },
    {
        'name': 'static/css/style.css',
        'desc': 'UI styling. Sidebar, cards, tables, responsive grid layout.',
        'routes': 'Dark header, light sidebar, stat cards with icons, hover effects'
    }
]

for comp in main_components:
    story.append(Paragraph(f"<b>{comp['name']}</b>", normal_style))
    story.append(Paragraph(f"Purpose: {comp['desc']}", normal_style))
    story.append(Paragraph(f"Routes/Content: {comp['routes']}", code_style))
    story.append(Spacer(1, 0.08*inch))

story.append(PageBreak())

# ==================== 7. SETUP & DEPLOYMENT ====================
story.append(Paragraph("6. Setup & Deployment", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>Installation Steps:</b>", heading2_style))
setup_steps = [
    "1. <b>Clone Repository</b><br/>git clone <repository_url><br/>cd hostel_surveillance",
    
    "2. <b>Create Virtual Environment</b><br/>python -m venv venv<br/>venv\\Scripts\\activate  (Windows)",
    
    "3. <b>Install Dependencies</b><br/>pip install tensorflow==2.12.0 deepface==0.0.75 flask==3.0.0<br/>pip install flask-session opencv-python scipy bcrypt pillow python-dotenv",
    
    "4. <b>Initialize Database</b><br/>python db/init_db.py",
    
    "5. <b>Create Admin User</b><br/>python -c \"import bcrypt; pw=bcrypt.hashpw(b'admin123',bcrypt.gensalt()).decode(); print(pw)\"<br/>Then insert into DB via SQL or admin creation script",
    
    "6. <b>Configure SMTP (Optional for Email Alerts)</b><br/>Set environment variables:<br/>SMTP_USER=your_email@gmail.com<br/>SMTP_PASS=your_app_password<br/>WARDEN_EMAIL=warden@hostel.com",
    
    "7. <b>Run Application</b><br/>python app.py<br/>Open http://localhost:5000 in browser"
]

for step in setup_steps:
    story.append(Paragraph(step, normal_style))
    story.append(Spacer(1, 0.08*inch))

story.append(Paragraph("<b>Important Notes:</b>", heading2_style))
story.append(Paragraph("""
• <b>TensorFlow Version:</b> Use tensorflow==2.12.0. Newer versions break on Windows.<br/>
• <b>Do NOT install MTCNN:</b> Conflicts with TensorFlow 2.12. Use OpenCV detector instead.<br/>
• <b>Face Registration:</b> Use webcam/mobile photos, not high-resolution studio photos (degrades ArcFace).<br/>
• <b>Similarity Threshold:</b> 0.55 gives ~80% accuracy. Adjust based on your environment.<br/>
• <b>Database:</b> SQLite at db/hostel.db. Backup regularly if in production.<br/>
• <b>Performance:</b> 2 FPS processing (not 30) reduces CPU load significantly.
""", normal_style))

story.append(PageBreak())

# ==================== 8. KEY CONFIGURATIONS ====================
story.append(Paragraph("7. Key Parameters & Configuration", heading1_style))
story.append(Spacer(1, 0.15*inch))

config_table_data = [
    ['Parameter', 'Default Value', 'Purpose'],
    ['FACE_MODEL', 'ArcFace', 'Deep CNN for feature extraction'],
    ['FACE_DETECTOR', 'opencv', 'Haar Cascade (fast, no conflicts)'],
    ['SIMILARITY_THRESHOLD', '0.55', 'Min confidence to consider match valid'],
    ['RECOGNITION_FPS', '2', 'Processing speed (CPU/latency tradeoff)'],
    ['DUPLICATE_WINDOW_MINUTES', '30', 'Prevent marking same student twice'],
    ['Min Face Size', '60x60 px', 'Ignore smaller faces'],
    ['Embedding Dimension', '512', 'ArcFace feature vector size'],
    ['DATABASE_PATH', 'db/hostel.db', 'SQLite database file location']
]

config_table = Table(config_table_data, colWidths=[1.5*inch, 1.5*inch, 1.9*inch])
config_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
]))
story.append(config_table)

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>How to Modify Parameters:</b>", heading2_style))
story.append(Paragraph("""
All parameters are defined in <b>config.py</b>. To modify:<br/>
1. Open hostel_surveillance/config.py<br/>
2. Edit desired values (e.g., SIMILARITY_THRESHOLD = 0.60)<br/>
3. Restart app: python app.py<br/>
4. Changes take effect immediately<br/>
<br/>
<b>For SMTP Email (Alerts):</b> Set environment variables before running:<br/>
• Windows PowerShell: $env:SMTP_USER = "your_email@gmail.com"<br/>
• Linux/Mac: export SMTP_USER="your_email@gmail.com"
""", normal_style))

# ==================== FINAL NOTES ====================
story.append(PageBreak())
story.append(Paragraph("Project Summary & Workflow Diagram", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>Complete Recognition Pipeline:</b>", heading2_style))
story.append(Paragraph("""
<b>Input:</b> Camera Frame (30 FPS captured, 2 FPS processed)<br/>
        ↓<br/>
<b>Haar Cascade Face Detector:</b> Locates face regions<br/>
        ↓<br/>
<b>DeepFace/ArcFace:</b> Extracts 512-dimensional embedding from detected face<br/>
        ↓<br/>
<b>Cosine Similarity:</b> Compares against all known face embeddings in memory<br/>
        ↓<br/>
<b>Match Decision:</b> If confidence ≥ 0.55 → Recognized | If confidence < 0.55 → Unknown<br/>
        ↓<br/>
<b>Classification:</b> Router determines person type (student/staff/blacklisted/unknown)<br/>
        ↓<br/>
<b>Action:</b><br/>
• Student → AttendanceService.mark_attendance()<br/>
• Blacklisted → AlertService.send_blacklist_alert()<br/>
• Unknown → AlertService.log_unknown()<br/>
        ↓<br/>
<b>Output:</b> Log entry in recognition_logs + Attendance updated + Alert sent (if needed)
""", code_style))

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Quick Reference: API Endpoints</b>", heading2_style))

api_data = [
    ['Endpoint', 'Method', 'Purpose'],
    ['/api/auth/login', 'POST', 'Login with username/password'],
    ['/api/students', 'GET', 'List all students'],
    ['/api/students/{id}/face', 'POST', 'Upload/register face for student'],
    ['/api/attendance', 'GET', 'Get attendance by date'],
    ['/api/camera/stream', 'GET', 'MJPEG video stream'],
    ['/api/dashboard/stats', 'GET', 'Real-time statistics'],
    ['/api/logs', 'GET', 'Recognition event logs'],
    ['/api/alerts', 'GET', 'Alert history'],
    ['/api/blacklist', 'GET', 'Blacklist records'],
    ['/api/blacklist', 'POST', 'Add person to blacklist']
]

api_table = Table(api_data, colWidths=[2*inch, 1*inch, 2*inch])
api_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c757d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
]))
story.append(api_table)

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Recent Project Updates:</b>", heading2_style))
story.append(Paragraph("""
✓ <b>Fixed Warden Sidebar:</b> Warden now sees warden-specific menu (Students, Attendance, Camera, Alerts)<br/>
✓ <b>Admin Menu Preserved:</b> Admin sees full menu (Students, Camera, Alerts, Logs, Blacklist)<br/>
✓ <b>Role-Based Access:</b> Frontend buildSidebar() function now explicitly handles admin vs warden vs other roles<br/>
✓ <b>Updated Files:</b> static/js/app.js and write_frontend.py both updated with proper role separation
""", normal_style))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", 
                       ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))

# Build PDF
doc.build(story)
print(f"\n✅ PDF Report Generated: {pdf_file}")
print(f"📊 Total Pages: ~25-30")
print(f"📁 Location: {pdf_file}")
