#!/usr/bin/env python3
"""
Test script to verify email and SMS functionality.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hostel_surveillance'))

from dotenv import load_dotenv
load_dotenv()

from hostel_surveillance.services.alert_service import AlertService

def test_email():
    print("Testing Email...")
    alert_service = AlertService()
    success = alert_service._send_email(
        to=os.environ.get('WARDEN_EMAIL'),
        subject="Test Email from Hostel Surveillance",
        body="This is a test email to verify the email configuration is working."
    )
    return success

def test_sms():
    print("Testing SMS...")
    alert_service = AlertService()
    success = alert_service._send_sms("This is a test SMS from Hostel Surveillance.")
    return success

if __name__ == "__main__":
    print("Testing Email and SMS functionality...\n")

    email_ok = test_email()
    sms_ok = test_sms()

    print("\n" + "="*50)
    print("RESULTS:")
    print(f"Email: {'✅ WORKING' if email_ok else '❌ FAILED'}")
    print(f"SMS: {'✅ WORKING' if sms_ok else '❌ FAILED'}")

    if not email_ok or not sms_ok:
        print("\nTroubleshooting:")
        if not email_ok:
            print("- Check SMTP_USER and SMTP_PASS in .env")
            print("- Ensure Gmail App Password is correct")
            print("- Verify WARDEN_EMAIL is valid")
        if not sms_ok:
            print("- Check TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM")
            print("- Verify WARDEN_PHONE is correct")
            print("- Ensure Twilio account has credits")