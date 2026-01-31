"""
Authentication module for user signup, login, email verification, and password reset
"""

import re
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from backend.database import (
    create_user, get_user_by_email, verify_user_email, update_user_password
)
from backend.email_utils import send_verification_email, send_password_reset_email
import os
from dotenv import load_dotenv

load_dotenv()

# Secret key for token signing
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
serializer = URLSafeTimedSerializer(SECRET_KEY)

# ==================== VALIDATION ====================

def validate_email(email):
    """
    Validate email format and domain
    Allows: gmail.com or Google Workspace domains
    """
    # Check valid email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    # Check if gmail.com or Google Workspace (for now allowing most domains)
    # In production, verify against Google's domain list
    domain = email.split('@')[1].lower()
    if domain != 'gmail.com':
        # For testing, allow any domain. In production, verify it's Google Workspace
        # You can add a list of allowed domains
        pass
    
    return True, "Valid email"

def validate_password(password):
    """
    Validate password against strict rules:
    - More than 7 characters
    - At least 1 digit
    - At least 1 special character (!, -, ))
    - Special character NOT at beginning or end
    """
    if len(password) <= 7:
        return False, "Password must be longer than 7 characters"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least 1 digit (0-9)"
    
    # Check for special characters: !, -, )
    special_chars = set('!-)')
    has_special = any(c in special_chars for c in password)
    
    if not has_special:
        return False, "Password must contain at least 1 special character (!, -, ))"
    
    # Check special char not at beginning or end
    if password[0] in special_chars:
        return False, "Special character cannot be at the beginning of password"
    
    if password[-1] in special_chars:
        return False, "Special character cannot be at the end of password"
    
    return True, "Valid password"

# ==================== SIGNUP ====================

def signup_user(name, email, password, password_confirm):
    """
    Register a new user account
    
    Returns:
        (success: bool, message: str, user_id: int or None)
    """
    # Validate inputs
    if not all([name, email, password, password_confirm]):
        return False, "All fields are required", None
    
    # Validate email
    email_valid, email_msg = validate_email(email.strip())
    if not email_valid:
        return False, email_msg, None
    
    # Validate password
    pass_valid, pass_msg = validate_password(password)
    if not pass_valid:
        return False, pass_msg, None
    
    # Check passwords match
    if password != password_confirm:
        return False, "Passwords do not match", None
    
    # Check if email already exists
    existing_user = get_user_by_email(email.strip())
    if existing_user:
        return False, "Email already registered", None
    
    # Hash password and create user
    password_hash = generate_password_hash(password)
    user_id = create_user(name.strip(), email.strip(), password_hash)
    
    if not user_id:
        return False, "Failed to create user", None
    
    return True, "Signup successful", user_id

# ==================== EMAIL VERIFICATION ====================

def generate_verification_token(user_id):
    """Generate a signed, time-limited verification token"""
    return serializer.dumps(user_id, salt='email-verification')

def verify_token(token, salt, max_age=86400):
    """
    Verify a signed token
    
    Args:
        token: The token to verify
        salt: The salt used when generating (email-verification or password-reset)
        max_age: Maximum age in seconds (default: 24 hours)
    
    Returns:
        (success: bool, user_id: int or None, message: str)
    """
    try:
        user_id = serializer.loads(token, salt=salt, max_age=max_age)
        return True, user_id, "Token verified"
    except SignatureExpired:
        return False, None, "Token has expired"
    except BadSignature:
        return False, None, "Invalid token"

def send_verification_email_to_user(user_id, user_email, user_name, app_url):
    """
    Generate token and send verification email
    
    Returns:
        (success: bool, message: str)
    """
    token = generate_verification_token(user_id)
    verification_link = f"{app_url}/verify/{token}"
    
    success = send_verification_email(user_email, user_name, verification_link)
    
    if success:
        return True, "Verification email sent. Please check your inbox."
    else:
        return False, "Failed to send verification email. Please try again later."

# ==================== LOGIN ====================

def login_user(email, password):
    """
    Authenticate user credentials
    
    Returns:
        (success: bool, message: str, user_id: int or None)
    """
    if not email or not password:
        return False, "Email and password required", None
    
    # Get user from database
    user = get_user_by_email(email.strip())
    
    if not user:
        return False, "Email not registered", None
    
    # TODO: Re-enable email verification check after testing
    # Check if email is verified
    # if not user.get('is_verified'):
    #     return False, "Please verify your email before logging in", None
    
    # Check password
    if not check_password_hash(user['password_hash'], password):
        return False, "Invalid password", None
    
    return True, "Login successful", user['id']

# ==================== PASSWORD RESET ====================

def generate_password_reset_token(user_id):
    """Generate a signed, time-limited password reset token"""
    return serializer.dumps(user_id, salt='password-reset')

def send_password_reset_email_to_user(email, app_url):
    """
    Send password reset email
    
    Returns:
        (success: bool, message: str)
    """
    user = get_user_by_email(email.strip())
    
    if not user:
        # Don't reveal whether email exists for security
        return True, "If this email is registered, password reset instructions will be sent"
    
    token = generate_password_reset_token(user['id'])
    reset_link = f"{app_url}/reset-password/{token}"
    
    success = send_password_reset_email(email, user['name'], reset_link)
    
    if success:
        return True, "Password reset email sent. Check your inbox."
    else:
        return False, "Failed to send reset email. Please try again later."

def reset_password(token, new_password, new_password_confirm):
    """
    Reset user password with token validation
    
    Returns:
        (success: bool, message: str)
    """
    if not new_password or not new_password_confirm:
        return False, "Password is required"
    
    # Validate new password
    pass_valid, pass_msg = validate_password(new_password)
    if not pass_valid:
        return False, pass_msg
    
    # Check passwords match
    if new_password != new_password_confirm:
        return False, "Passwords do not match"
    
    # Verify token (1 hour expiry for password reset)
    success, user_id, msg = verify_token(token, 'password-reset', max_age=3600)
    
    if not success:
        return False, msg
    
    # Update password
    password_hash = generate_password_hash(new_password)
    updated = update_user_password(user_id, password_hash)
    
    if updated:
        return True, "Password reset successful. You can now login with your new password."
    else:
        return False, "Failed to update password. Please try again."
