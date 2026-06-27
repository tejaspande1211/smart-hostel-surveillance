# Email & SMS Alert Setup Guide

## ✅ What's Already Implemented

Your `alert_service.py` already has complete functionality for:
- **Unknown Face Detection**: Sends email + SMS when unknown person detected (3 detections in 12 seconds)
- **Blacklisted Person Detection**: Sends immediate email + SMS when blacklisted person detected

## 🔐 Security Fixed

1. **Removed hardcoded credentials** from `config.py`
2. **All sensitive data now uses environment variables only** (from `.env` file)
3. **Created `.env` file** (ignored by git) for local configuration

## 📋 Setup Instructions

### Step 1: Configure Gmail (Email Alerts)

1. Enable 2-Factor Authentication on Gmail: https://myaccount.google.com/security
2. Get App Password: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

3. Fill in `.env` file:
   ```
   SMTP_USER=your_gmail@gmail.com
   SMTP_PASS=xxxx xxxx xxxx xxxx  (your app password)
   WARDEN_EMAIL=warden@example.com
   ```

### Step 2: Configure Twilio (SMS Alerts) - Optional

1. Create Twilio account: https://www.twilio.com/console
2. Get credentials:
   - Account SID
   - Auth Token
   - Phone number (starting with +1...)
3. Fill in `.env` file:
   ```
   TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_TOKEN=your_auth_token
   TWILIO_FROM=+1234567890
   WARDEN_PHONE=+911234567890
   ```

**OR** Use SMS Gateway (alternative):
```
SMS_GATEWAY_DOMAIN=sms.example.com
WARDEN_PHONE=8010679493
```

### Step 3: Verify Configuration

Run before starting the app:
```bash
python verify_setup.py
```

This will check if all required credentials are set.

## 🚀 How Alerts Work

### Unknown Face Detection
```
Frame 1 (unknown) → logged
Frame 2 (unknown) → logged
Frame 3 (unknown) → ✉️ EMAIL + 📱 SMS SENT
(3 detections within 12 seconds)
```

### Blacklisted Person Detection
```
Face detected → Immediately ✉️ EMAIL + 📱 SMS SENT
(no delay)
```

## 📧 Email Contents

**Blacklist Alert:**
```
Subject: ALERT: Restricted Person Detected - [NAME]
Body:
  SECURITY ALERT
  A restricted/blacklisted person entered the area.
  Name: [NAME]
  Reason: [REASON]
  Time: [TIMESTAMP]
  Attachment: Captured frame
```

**Unknown Alert:**
```
Subject: ALERT: Unknown Person Detected
Body:
  SECURITY ALERT
  An unknown/unrestricted person detected in multiple frames.
  Time: [TIMESTAMP]
  Attachment: Captured frame
```

## 📱 SMS Contents

**Blacklist:** `RESTRICTED PERSON ENTERED: [NAME] at [TIME]`

**Unknown:** `UNKNOWN PERSON ENTERED at [TIME]`

## ✅ Files Modified/Created

- `config.py` - Removed hardcoded credentials ✓
- `app.py` - Added `.env` file loader ✓
- `.env` - Local credentials (gitignored) ✓
- `.env.example` - Template for setup ✓
- `verify_setup.py` - Configuration checker ✓

## 🧪 Testing Alerts

```python
from services.alert_service import AlertService
from db.db_manager import DatabaseManager
import cv2
import numpy as np

alert_service = AlertService()

# Test frame
test_frame = np.zeros((480, 640, 3), dtype=np.uint8)

# Test unknown alert
alert_service.log_unknown(test_frame)  # Repeat 3x to trigger alert

# Test blacklist alert
alert_service.send_blacklist_alert(person_id=1, frame=test_frame)
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Email not sending | Check Gmail App Password is correct (16 chars with spaces) |
| SMS not sending | Check Twilio credentials or configure SMS Gateway |
| 401 Auth Error (Email) | App Password must be for Gmail (not regular password) |
| Invalid phone format | Use international format: +919999999999 |
| ".env not found" error | Run from project root directory |

## 🛡️ Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] `.env` is NOT committed to git
- [ ] Using Gmail App Password (not regular password)
- [ ] Phone numbers include country codes
- [ ] Credentials are in `.env` file only, not in code

---

**All set! Run `python verify_setup.py` to confirm everything is working.** ✅
