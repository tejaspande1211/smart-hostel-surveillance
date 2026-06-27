#!/usr/bin/env python3
"""
Verify that config and environment variables are correctly set up.
Run this before starting the app: python verify_setup.py
"""
import os
import sys

def verify_config():
    print("\n" + "="*60)
    print("HOSTEL SURVEILLANCE CONFIGURATION VERIFICATION")
    print("="*60 + "\n")
    
    # Load .env file
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    
    issues = []
    
    # Check SMTP Configuration
    print("📧 SMTP EMAIL CONFIGURATION:")
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    warden_email = os.environ.get('WARDEN_EMAIL')
    
    if smtp_user:
        print(f"  ✓ SMTP_USER: {smtp_user}")
    else:
        print(f"  ✗ SMTP_USER: NOT SET")
        issues.append("SMTP_USER not configured")
    
    if smtp_pass:
        print(f"  ✓ SMTP_PASS: {'*' * len(smtp_pass)}")
    else:
        print(f"  ✗ SMTP_PASS: NOT SET")
        issues.append("SMTP_PASS not configured")
    
    if warden_email:
        print(f"  ✓ WARDEN_EMAIL: {warden_email}")
    else:
        print(f"  ✗ WARDEN_EMAIL: NOT SET")
        issues.append("WARDEN_EMAIL not configured")
    
    # Check SMS Configuration
    print("\n📱 TWILIO SMS CONFIGURATION:")
    twilio_sid = os.environ.get('TWILIO_SID')
    twilio_token = os.environ.get('TWILIO_TOKEN')
    twilio_from = os.environ.get('TWILIO_FROM')
    warden_phone = os.environ.get('WARDEN_PHONE')
    sms_gateway = os.environ.get('SMS_GATEWAY_DOMAIN')
    
    if twilio_sid or sms_gateway:
        if twilio_sid:
            print(f"  ✓ TWILIO_SID: {twilio_sid[:10]}...")
            if twilio_token:
                print(f"  ✓ TWILIO_TOKEN: {'*' * 10}")
            else:
                print(f"  ✗ TWILIO_TOKEN: NOT SET")
                issues.append("TWILIO_TOKEN not configured")
            
            if twilio_from:
                print(f"  ✓ TWILIO_FROM: {twilio_from}")
            else:
                print(f"  ✗ TWILIO_FROM: NOT SET")
                issues.append("TWILIO_FROM not configured")
        else:
            print(f"  ℹ  TWILIO_SID: Not configured (using SMS Gateway)")
            print(f"  ✓ SMS_GATEWAY_DOMAIN: {sms_gateway}")
        
        if warden_phone:
            print(f"  ✓ WARDEN_PHONE: {warden_phone}")
        else:
            print(f"  ✗ WARDEN_PHONE: NOT SET")
            issues.append("WARDEN_PHONE not configured")
    else:
        print(f"  ℹ  SMS: No configuration found (optional)")
    
    # Summary
    print("\n" + "="*60)
    if issues:
        print("❌ CONFIGURATION ISSUES FOUND:")
        for issue in issues:
            print(f"  • {issue}")
        print("\n💡 SOLUTION:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your credentials in .env file")
        print("  3. For Gmail: Get App Password from https://myaccount.google.com/apppasswords")
        print("  4. For Twilio: Get credentials from https://www.twilio.com/console")
        return False
    else:
        print("✅ CONFIGURATION VERIFIED SUCCESSFULLY!")
        print("All required settings are configured. You're ready to run the app.")
        return True
    
    print("="*60 + "\n")

if __name__ == "__main__":
    success = verify_config()
    sys.exit(0 if success else 1)
