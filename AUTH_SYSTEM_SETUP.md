# MarketMind - Complete Authentication + User Activity History System

## Overview
This system implements a **production-quality authentication and user activity tracking system** similar to Chrome, Google, and ChatGPT. It uses Flask sessions, SQLite, and Gmail SMTP for email verification.

## ✅ IMPLEMENTATION COMPLETE

### What's Implemented

#### 1. **DATABASE SCHEMA** (`backend/database.py`)
- ✅ **users table**: id, name, email, password_hash, is_verified, created_at, updated_at
- ✅ **user_history table**: id, user_id, page_url, page_title, action_type, metadata (JSON), timestamp, ip_address, user_agent
- ✅ Indexes for fast queries: user_id, timestamp, email
- ✅ Foreign key relationships with ON DELETE CASCADE

#### 2. **AUTHENTICATION MODULE** (`backend/auth.py`)
- ✅ **Signup**: Email validation, password validation (strict rules), duplicate email checking
- ✅ **Email Verification**: Signed time-limited tokens (24 hour expiry)
- ✅ **Login**: Email verification required, password hash validation
- ✅ **Forgot Password**: Time-limited reset tokens (1 hour expiry)
- ✅ **Password Reset**: With token validation and new password rules

**Password Rules (Strict)**:
- More than 7 characters
- At least 1 digit (0-9)
- At least 1 special character (!, -, ))
- Special character NOT at beginning or end

#### 3. **EMAIL SERVICE** (`backend/email_utils.py`)
- ✅ Gmail SMTP integration (smtp.gmail.com:465)
- ✅ HTML-formatted emails
- ✅ Verification email with clickable link
- ✅ Password reset email with clickable link
- ✅ Error handling and logging

#### 4. **HISTORY TRACKING** (`backend/history.py`)
- ✅ Automatic activity logging for authenticated users only
- ✅ Tracks: login, logout, page visits, password reset, form submissions
- ✅ Grouped by date: Today, Yesterday, This week, Older
- ✅ JSON metadata support
- ✅ Delete individual items or clear all history

#### 5. **FLASK ROUTES** (`app.py`)
- ✅ **Authentication Routes**:
  - POST `/signup` - User registration
  - GET `/verify/<token>` - Email verification
  - POST/GET `/login` - User login
  - `/logout` - User logout
  - POST/GET `/forgot-password` - Password reset request
  - POST/GET `/reset-password/<token>` - Password reset form
  
- ✅ **Protected Routes** (require login):
  - `/` - Home page
  - `/campaign` - Campaign generator
  - `/pitch` - Sales pitch generator
  - `/lead-score` - Lead scoring
  - `/history` - User activity history

- ✅ **API Endpoints** (authenticated):
  - POST `/api/generate-campaign` - Generate campaign with history logging
  - POST `/api/generate-pitch` - Generate pitch with history logging
  - POST `/api/score-lead` - Score lead with history logging
  - GET `/api/history/grouped` - Get grouped history
  - DELETE `/api/history/delete/<id>` - Delete history item
  - DELETE `/api/history/clear` - Clear all history

#### 6. **FRONTEND TEMPLATES**
- ✅ `signup.html` - Beautiful signup form with password rules display
- ✅ `login.html` - Login with "Forgot Password?" link
- ✅ `forgot_password.html` - Password reset request form
- ✅ `reset_password.html` - Password reset form with token validation
- ✅ `verification_pending.html` - Email verification pending message
- ✅ `verify_success.html` - Email verified success page
- ✅ `verify_error.html` - Email verification error page
- ✅ `password_reset_sent.html` - Reset email sent confirmation
- ✅ `reset_password_success.html` - Password reset success page
- ✅ `reset_password_error.html` - Password reset error page

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Install Dependencies
```bash
pip install flask flask-session werkzeug itsdangerous python-dotenv
```

### Step 2: Configure Gmail SMTP

1. **Enable Gmail 2-Step Verification**:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

3. **Update `.env`** file:
   ```env
   GROQ_API_KEY=your_groq_key
   SECRET_KEY=your-secret-key-change-in-production
   GMAIL_ADDRESS=your-email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   APP_URL=http://127.0.0.1:5000
   ```

### Step 3: Initialize Database
```python
from backend.database import init_database
init_database()
```

### Step 4: Run the Application
```bash
python app.py
```

Server runs on: `http://127.0.0.1:5000`

---

## 📊 USER FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                      │
└─────────────────────────────────────────────────────────────┘

1. NEW USER (SIGNUP)
   /signup 
   → Validate inputs
   → Hash password
   → Create user (is_verified = false)
   → Send verification email
   → Show "Check Email" page

2. EMAIL VERIFICATION
   Click link in email
   → Verify token (24h expiry)
   → Mark user as verified
   → Show "Verified" page
   → Ready to login

3. EXISTING USER (LOGIN)
   /login
   → Validate email exists
   → Check email verified
   → Verify password hash
   → Create session
   → Log "login" activity
   → Redirect to home

4. FORGOT PASSWORD
   /forgot-password
   → User enters email
   → Generate reset token (1h expiry)
   → Send reset email
   → Show "Check Email" page

5. RESET PASSWORD
   Click link in email
   → Verify token (1h expiry)
   → User enters new password
   → Validate password rules
   → Hash and update
   → Show "Success" page
   → Ready to login

6. PROTECTED PAGES
   /campaign, /pitch, /lead-score, /history
   → Check session.logged_in_user_id
   → If missing → Redirect to /login
   → If exists → Load page + user data
   → Log all activities automatically
```

---

## 🔐 SECURITY FEATURES

✅ **Password Security**:
- Passwords hashed using Werkzeug PBKDF2
- Strict password rules enforced
- No plaintext passwords stored

✅ **Token Security**:
- Signed tokens using itsdangerous
- Time-limited (email: 24h, reset: 1h)
- One-time use (token deleted after verification)

✅ **Session Security**:
- Session cookies HttpOnly
- Secure flag can be enabled for HTTPS
- 1-year session lifetime (configurable)

✅ **Input Validation**:
- Email format validation
- Domain validation (Gmail focused)
- Required field validation
- Sanitized inputs

✅ **Cross-User Protection**:
- Users can only access own history
- Delete/clear operations verified by user_id
- No unauthorized access possible

✅ **Rate Limiting** (recommended future):
- Add flask-limiter for login attempts
- Add email sending limits

---

## 📋 DATABASE SCHEMA

### users table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);
```

### user_history table
```sql
CREATE TABLE user_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    page_url TEXT NOT NULL,
    page_title TEXT,
    action_type TEXT NOT NULL,
    metadata TEXT,  -- JSON
    timestamp DATETIME,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### action_type values
- `login` - User logged in
- `logout` - User logged out
- `visit` - Visited a page
- `campaign_generated` - Generated marketing campaign
- `pitch_generated` - Generated sales pitch
- `lead_scored` - Scored a lead
- `history_cleared` - Cleared all history
- `password_reset` - Reset password

---

## 🧪 TESTING

### Test Signup Flow
1. Go to `http://127.0.0.1:5000/signup`
2. Enter: name, email, password (must follow rules)
3. Click "Create Account"
4. Check console for email verification link (since SMTP might not be configured)
5. Click verification link

### Test Login
1. Go to `http://127.0.0.1:5000/login`
2. Enter email and password
3. Should redirect to home page
4. Check history - login should be logged

### Test Protected Pages
1. Try accessing `/campaign` without login
2. Should redirect to `/login`
3. Login first, then access `/campaign`
4. Try generating a campaign
5. Go to `/history` to see logged activity

### Test History
1. Generate a campaign/pitch/lead score
2. Go to `/history`
3. Should see all activities grouped by date
4. Click to expand and see details
5. Test delete and clear functionality

### Test Forgot Password
1. Go to `http://127.0.0.1:5000/forgot-password`
2. Enter registered email
3. Click reset link in email
4. Enter new password (must follow rules)
5. Should redirect to login
6. Login with new password

---

## 📁 FILE STRUCTURE

```
MarketMind/
├── app.py                              # Flask app with all routes
├── .env                                # Configuration (secret, email)
├── backend/
│   ├── __init__.py
│   ├── database.py                     # Database operations (UPDATED)
│   ├── auth.py                         # Authentication logic (NEW)
│   ├── history.py                      # History tracking (NEW)
│   ├── email_utils.py                  # Email sending (NEW)
│   ├── ai_engine.py                    # AI integration
│   ├── prompts.py                      # Prompt templates
│   └── __pycache__/
├── frontend/
│   ├── templates/
│   │   ├── base.html                   # Base template
│   │   ├── index.html                  # Home page
│   │   ├── campaign.html               # Campaign page
│   │   ├── pitch.html                  # Pitch page
│   │   ├── lead-score.html             # Lead score page
│   │   ├── history.html                # History page
│   │   ├── signup.html                 # Signup (NEW)
│   │   ├── login.html                  # Login (NEW)
│   │   ├── forgot_password.html        # Forgot password (NEW)
│   │   ├── reset_password.html         # Reset password (NEW)
│   │   ├── verification_pending.html   # Pending verification (NEW)
│   │   ├── verify_success.html         # Verification success (NEW)
│   │   ├── verify_error.html           # Verification error (NEW)
│   │   ├── password_reset_sent.html    # Reset sent (NEW)
│   │   ├── reset_password_success.html # Reset success (NEW)
│   │   └── reset_password_error.html   # Reset error (NEW)
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   ├── modern.css
│   │   └── js/
│   │       ├── main.js
│   │       ├── modern.js
│   │       └── history-tracker.js
│   └── __pycache__/
├── marketmind.db                       # SQLite database
├── requirements.txt
└── README.md
```

---

## 🔧 CONFIGURATION

### .env Example
```env
# AI
GROQ_API_KEY=gsk_...

# Authentication
SECRET_KEY=dev-secret-key-change-in-production

# Email (Gmail)
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# App URL
APP_URL=http://127.0.0.1:5000
```

---

## 🚨 IMPORTANT NOTES

1. **Gmail App Password Required**:
   - Cannot use regular password
   - Must generate App Password in Google Account
   - Works only with Gmail (Google Workspace supported)

2. **Email Testing**:
   - If SMTP fails, check credentials in `.env`
   - Verify Gmail 2-Step is enabled
   - Check that "Less secure apps" is OFF

3. **Production Deployment**:
   - Change SECRET_KEY to a strong random value
   - Set SESSION_COOKIE_SECURE = True (HTTPS only)
   - Use proper domain for APP_URL
   - Consider adding rate limiting
   - Use environment variables for sensitive data

4. **Token Expiry**:
   - Email verification: 24 hours
   - Password reset: 1 hour
   - Can be adjusted in `auth.py`

---

## 🎯 NEXT STEPS

1. Configure Gmail SMTP in `.env`
2. Run `python app.py`
3. Visit `http://127.0.0.1:5000/signup`
4. Test the complete flow
5. Check database: `sqlite3 marketmind.db`

---

## 📞 SUPPORT

If you encounter issues:
1. Check console for error messages
2. Verify `.env` configuration
3. Ensure Gmail 2-Step is enabled
4. Check database exists and has tables
5. Review logs in Flask console

---

**System Status**: ✅ READY FOR USE
**Last Updated**: January 31, 2026
