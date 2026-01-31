#!/usr/bin/env python3
"""
MarketMind Authentication System Verification Script
Checks if all components are properly configured and ready
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("MarketMind Authentication System - Verification Check")
print("=" * 70)

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
CHECK = '✓'
CROSS = '✗'

checks_passed = 0
checks_failed = 0

def check(condition, message, details=""):
    global checks_passed, checks_failed
    if condition:
        print(f"{GREEN}{CHECK}{RESET} {message}")
        if details:
            print(f"  → {details}")
        checks_passed += 1
    else:
        print(f"{RED}{CROSS}{RESET} {message}")
        if details:
            print(f"  → {details}")
        checks_failed += 1

print("\n1️⃣  CHECKING FILE STRUCTURE")
print("-" * 70)

# Check core files
check(
    os.path.exists("app.py"),
    "app.py exists",
    "Flask application entry point"
)

check(
    os.path.exists("backend/auth.py"),
    "backend/auth.py exists",
    "Authentication module (signup, login, verification, password reset)"
)

check(
    os.path.exists("backend/database.py"),
    "backend/database.py exists",
    "Database operations and schema"
)

check(
    os.path.exists("backend/email_utils.py"),
    "backend/email_utils.py exists",
    "Gmail SMTP email sending module"
)

check(
    os.path.exists("backend/history.py"),
    "backend/history.py exists",
    "User activity history tracking"
)

check(
    os.path.exists("frontend/templates/signup.html"),
    "frontend/templates/signup.html exists",
    "User signup form template"
)

check(
    os.path.exists("frontend/templates/login.html"),
    "frontend/templates/login.html exists",
    "User login form template"
)

print("\n2️⃣  CHECKING CONFIGURATION")
print("-" * 70)

# Check .env file
check(
    os.path.exists(".env"),
    ".env configuration file exists",
    "Environment variables for authentication"
)

# Check environment variables
groq_key = os.getenv('GROQ_API_KEY')
secret_key = os.getenv('SECRET_KEY')
gmail_addr = os.getenv('GMAIL_ADDRESS')
gmail_pass = os.getenv('GMAIL_APP_PASSWORD')
app_url = os.getenv('APP_URL')

check(
    groq_key and groq_key != '',
    "GROQ_API_KEY is configured",
    f"Key starts with: {groq_key[:10]}..." if groq_key else "Not set"
)

check(
    secret_key and secret_key != '' and secret_key != 'dev-secret-key-change-in-production',
    "SECRET_KEY is configured (not default)",
    "Used for session signing"
)

check(
    gmail_addr and gmail_addr != 'your-gmail@gmail.com',
    "GMAIL_ADDRESS is configured",
    f"Email: {gmail_addr}"
)

check(
    gmail_pass and gmail_pass != 'your-app-password',
    "GMAIL_APP_PASSWORD is configured",
    "Gmail App Password set (not default)"
)

check(
    app_url and app_url != '',
    "APP_URL is configured",
    f"URL: {app_url}"
)

print("\n3️⃣  CHECKING PYTHON DEPENDENCIES")
print("-" * 70)

dependencies = [
    ("flask", "Flask"),
    ("flask_session", "Flask-Session"),
    ("werkzeug", "Werkzeug"),
    ("itsdangerous", "itsdangerous"),
    ("dotenv", "python-dotenv"),
    ("sqlite3", "sqlite3 (built-in)"),
]

for module_name, display_name in dependencies:
    try:
        __import__(module_name)
        check(True, f"{display_name} is installed")
    except ImportError:
        check(False, f"{display_name} is installed", "Run: pip install -r requirements.txt")

print("\n4️⃣  CHECKING DATABASE")
print("-" * 70)

try:
    from backend.database import get_db
    
    # Try to connect to database
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_exists = cursor.fetchone() is not None
        check(users_exists, "users table exists in database")
        
        # Check user_history table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_history'")
        history_exists = cursor.fetchone() is not None
        check(history_exists, "user_history table exists in database")
        
        if users_exists and history_exists:
            # Get table stats
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_history")
            history_count = cursor.fetchone()[0]
            
            print(f"\n  Database Statistics:")
            print(f"  → Users registered: {user_count}")
            print(f"  → History records: {history_count}")
            
except Exception as e:
    check(False, "Database connection failed", str(e))

print("\n5️⃣  CHECKING AUTHENTICATION MODULES")
print("-" * 70)

try:
    from backend.auth import (
        validate_email,
        validate_password,
        signup_user,
        login_user,
        send_verification_email_to_user,
        verify_token,
        send_password_reset_email_to_user,
        reset_password
    )
    check(True, "All authentication functions imported successfully")
    
    # Test password validation
    result = validate_password("Test@123")
    check(result[0], "Password validation working", "Accepts 'Test@123'")
    
    # Test email validation
    result = validate_email("test@gmail.com")
    check(result[0], "Email validation working", "Accepts 'test@gmail.com'")
    
except ImportError as e:
    check(False, "Authentication module import failed", str(e))
except Exception as e:
    check(False, "Authentication validation failed", str(e))

print("\n6️⃣  CHECKING HISTORY TRACKING")
print("-" * 70)

try:
    from backend.history import (
        log_user_activity,
        get_grouped_user_history,
        delete_history_item,
        clear_user_history
    )
    check(True, "All history functions imported successfully")
except ImportError as e:
    check(False, "History module import failed", str(e))

print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

total_checks = checks_passed + checks_failed
print(f"\n{GREEN}✓ Passed: {checks_passed}{RESET}")
print(f"{RED}✗ Failed: {checks_failed}{RESET}")
print(f"Total: {total_checks} checks\n")

if checks_failed == 0:
    print(f"{GREEN}🎉 ALL CHECKS PASSED! System is ready to use.{RESET}\n")
    print("Next steps:")
    print("1. Configure GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env")
    print("2. Run: python app.py")
    print("3. Visit: http://127.0.0.1:5000/signup")
    sys.exit(0)
else:
    print(f"{RED}⚠️  SOME CHECKS FAILED. Please fix the issues above.{RESET}\n")
    print("Troubleshooting:")
    print("1. Check .env configuration")
    print("2. Run: pip install -r requirements.txt")
    print("3. Ensure database directory exists")
    sys.exit(1)
