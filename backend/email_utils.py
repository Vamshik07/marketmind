"""
Email utilities for sending verification and password reset emails
Uses Gmail SMTP with App Passwords
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
APP_URL = os.getenv('APP_URL', 'http://127.0.0.1:5000')

def send_email(to_email, subject, html_body):
    """
    Send an email using Gmail SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML email body
    
    Returns:
        True if successful, False otherwise
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("ERROR: Gmail credentials not configured. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach HTML body
        part = MIMEText(html_body, 'html')
        msg.attach(part)
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"ERROR sending email to {to_email}: {str(e)}")
        return False

def send_verification_email(user_email, user_name, verification_link):
    """
    Send email verification link
    
    Args:
        user_email: User's email address
        user_name: User's name
        verification_link: Full URL to verification endpoint
    
    Returns:
        True if successful, False otherwise
    """
    subject = "Verify Your MarketMind Account"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #f8f9fc; padding: 20px; border-radius: 8px;">
                <h2 style="color: #223CCF; margin-top: 0;">Welcome to MarketMind! 🚀</h2>
                
                <p>Hi {user_name},</p>
                
                <p>Thank you for signing up. To complete your registration and start using MarketMind, 
                please verify your email address by clicking the button below.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background-color: #223CCF; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 6px; display: inline-block;
                              font-weight: bold;">
                        ✓ Verify Email Address
                    </a>
                </div>
                
                <p style="font-size: 12px; color: #999;">
                    Or copy and paste this link in your browser:<br>
                    <code style="background-color: #eee; padding: 2px 6px; border-radius: 3px;">
                        {verification_link}
                    </code>
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #999;">
                    This verification link will expire in 24 hours.<br>
                    If you did not create this account, please ignore this email.
                </p>
                
                <p style="color: #999; font-size: 12px; margin-top: 20px;">
                    Best regards,<br>
                    <strong>MarketMind Team</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(user_email, subject, html_body)

def send_password_reset_email(user_email, user_name, reset_link):
    """
    Send password reset link
    
    Args:
        user_email: User's email address
        user_name: User's name
        reset_link: Full URL to password reset endpoint
    
    Returns:
        True if successful, False otherwise
    """
    subject = "Reset Your MarketMind Password"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #f8f9fc; padding: 20px; border-radius: 8px;">
                <h2 style="color: #223CCF; margin-top: 0;">Password Reset Request 🔐</h2>
                
                <p>Hi {user_name},</p>
                
                <p>We received a request to reset the password for your MarketMind account. 
                Click the button below to create a new password.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background-color: #ED3D63; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 6px; display: inline-block;
                              font-weight: bold;">
                        🔄 Reset Password
                    </a>
                </div>
                
                <p style="font-size: 12px; color: #999;">
                    Or copy and paste this link in your browser:<br>
                    <code style="background-color: #eee; padding: 2px 6px; border-radius: 3px;">
                        {reset_link}
                    </code>
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #999;">
                    This password reset link will expire in 1 hour.<br>
                    If you did not request a password reset, please ignore this email 
                    and your password will remain unchanged.
                </p>
                
                <p style="color: #999; font-size: 12px; margin-top: 20px;">
                    Best regards,<br>
                    <strong>MarketMind Team</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(user_email, subject, html_body)
