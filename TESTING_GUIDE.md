# MarketMind Authentication System - Testing Guide

## Quick Start

### Prerequisites
1. Python 3.8+
2. Flask and dependencies installed (`pip install -r requirements.txt`)
3. Gmail account with App Password configured

### Configuration (Critical!)

Edit `.env` file:
```env
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
SECRET_KEY=your-secret-key-here
APP_URL=http://127.0.0.1:5000
```

### Run Verification
```bash
python verify_system.py
```

### Start the Server
```bash
python app.py
```

Server runs on: `http://127.0.0.1:5000`

---

## Test Scenarios

### Test 1: User Registration (Signup)

**Purpose**: Verify signup form validation and user creation

**Steps**:
1. Go to: `http://127.0.0.1:5000/signup`
2. Enter test data:
   - Name: `John Doe`
   - Email: `john.doe@gmail.com` (use real Gmail for email verification)
   - Password: `Test@Pass123` (must follow rules)
   - Confirm Password: `Test@Pass123`
3. Click "Create Account"

**Expected Outcome**:
- ✅ Form validates password meets requirements
- ✅ User created in database
- ✅ Verification email sent
- ✅ Redirect to "Check Email" page
- ✅ Email received in inbox

**Validation Checks**:
- [ ] Invalid email formats rejected (e.g., "invalid", "test@.com")
- [ ] Weak passwords rejected (e.g., "pass", "123456")
- [ ] Duplicate email rejected (register twice)
- [ ] All fields required

---

### Test 2: Email Verification

**Purpose**: Verify email verification token workflow

**Steps**:
1. From signup, user receives verification email
2. Click verification link (contains signed token)
3. Page shows success message

**Expected Outcome**:
- ✅ Token validates (24h expiry)
- ✅ User marked as verified in database
- ✅ Success page shown
- ✅ User can now login

**Token Tests**:
- [ ] Valid token: Works and marks user verified
- [ ] Invalid token: Shows error page
- [ ] Expired token: Shows error with retry link
- [ ] Tampered token: Shows error

---

### Test 3: User Login

**Purpose**: Verify login authentication and session creation

**Steps**:
1. Go to: `http://127.0.0.1:5000/login`
2. Enter verified user credentials:
   - Email: `john.doe@gmail.com`
   - Password: `Test@Pass123`
3. Click "Sign In"

**Expected Outcome**:
- ✅ Credentials verified
- ✅ Session created
- ✅ Redirect to home page
- ✅ Login activity logged to history
- ✅ User name appears in navigation

**Login Tests**:
- [ ] Valid credentials: Login succeeds
- [ ] Wrong password: Error shown
- [ ] Non-existent email: Error shown
- [ ] Unverified user: Error shown
- [ ] Session persists on page reload

---

### Test 4: Protected Routes (Authentication)

**Purpose**: Verify that routes require login

**Steps**:
1. Open new incognito/private window (no session)
2. Try to access: `http://127.0.0.1:5000/campaign`
3. Should redirect to login

**Protected Routes to Test**:
- [ ] `/` (home)
- [ ] `/campaign` (campaign generator)
- [ ] `/pitch` (pitch generator)
- [ ] `/lead-score` (lead scoring)
- [ ] `/history` (history page)

**Expected Outcome**:
- ✅ All protected pages redirect to login
- ✅ After login, pages accessible
- ✅ User context available (`{{ user }}` template variable)

---

### Test 5: Activity History Logging

**Purpose**: Verify that user activities are tracked

**Steps**:
1. Login as verified user
2. Visit different pages:
   - Navigate to `/campaign`
   - Generate a campaign
   - Navigate to `/pitch`
   - Generate a pitch
3. Go to `/history`

**Expected Outcome**:
- ✅ All activities logged
- ✅ Grouped by date (Today, Yesterday, This week, Older)
- ✅ Shows action type (visit, campaign_generated, etc.)
- ✅ Timestamps are correct
- ✅ Only current user's history shown

**History Tests**:
- [ ] Activities logged automatically
- [ ] Can expand to see full details
- [ ] Can delete individual items
- [ ] Can clear all history
- [ ] Can copy output to clipboard
- [ ] Can download as text file

---

### Test 6: Logout

**Purpose**: Verify session termination

**Steps**:
1. While logged in, click "Logout" button
2. Session should be cleared
3. Try to access protected page

**Expected Outcome**:
- ✅ Session cleared
- ✅ Logout activity logged
- ✅ Redirect to login page
- ✅ Protected pages inaccessible

---

### Test 7: Forgot Password Flow

**Purpose**: Verify password reset workflow

**Steps**:
1. Go to: `http://127.0.0.1:5000/login`
2. Click "Forgot password?"
3. Enter email: `john.doe@gmail.com`
4. Click "Send Reset Link"

**Expected Outcome**:
- ✅ Email sent (regardless of email existence - security)
- ✅ Confirmation page shown
- ✅ Email received in inbox

---

### Test 8: Password Reset

**Purpose**: Verify password reset with token

**Steps**:
1. From "forgot password", user receives reset email
2. Click reset link (contains signed token)
3. Enter new password: `NewPass@456`
4. Confirm password
5. Click "Reset Password"

**Expected Outcome**:
- ✅ Token validates (1h expiry)
- ✅ Password meets validation rules
- ✅ Password updated in database
- ✅ Success page shown
- ✅ Can login with new password

**Token Tests**:
- [ ] Valid token: Works and resets password
- [ ] Invalid token: Shows error page
- [ ] Expired token: Shows error with new request link
- [ ] New password validates rules

---

### Test 9: Password Security

**Purpose**: Verify password validation rules

**Test Cases**:
```
Valid passwords:
✓ Test@Pass123
✓ MyPassword!
✓ Secret-Pass99
✓ A1bC2dE3-fGh!

Invalid passwords:
✗ test           (too short, no special char)
✗ password       (no number, no special char)
✗ 123456         (no letter, no special char)
✗ !MyPass123     (special char at start)
✗ MyPass123!     (special char at end)
✗ MyPass123@     (special char @, needs !, -, or ))
```

**Expected Outcome**:
- ✅ Strict rules enforced on signup and password reset
- ✅ Rules displayed clearly to user
- ✅ Error messages helpful

---

### Test 10: Database Operations

**Purpose**: Verify database integrity

**Steps**:
1. Use SQLite command line:
   ```bash
   sqlite3 marketmind.db
   ```

2. Check users table:
   ```sql
   SELECT id, name, email, is_verified FROM users;
   ```

3. Check history table:
   ```sql
   SELECT user_id, action_type, timestamp FROM user_history ORDER BY timestamp DESC LIMIT 10;
   ```

**Expected Outcome**:
- ✅ Users table contains registered users
- ✅ Passwords are hashed (not plaintext)
- ✅ User history grouped by user_id
- ✅ Timestamps are UTC format
- ✅ Foreign key constraints work

---

## Test Data Credentials

Use these for testing (after signup):

```
Email: test@gmail.com
Password: Test@Pass123
```

Or create your own with:
- Email: your-email@gmail.com
- Password: YourPass@123 (must follow rules)

---

## Troubleshooting

### Issue: Email not received
**Solution**:
1. Check GMAIL_ADDRESS is correct
2. Check GMAIL_APP_PASSWORD is valid
3. Check Gmail "Less secure apps" is OFF
4. Check email spam folder
5. Check Flask console for errors

### Issue: Login fails
**Solution**:
1. Verify email verified (check users table: `is_verified = 1`)
2. Check password is correct
3. Clear cookies and try again
4. Check database connection

### Issue: History not showing
**Solution**:
1. Verify user_id matches in history and users tables
2. Check action_type is being logged
3. Check timestamps are valid
4. Try different date filters

### Issue: Password reset email not received
**Solution**:
1. Same as email issues above
2. Check token validity (1 hour max)
3. Verify email in forgot-password form is exact

### Issue: Protected pages still accessible without login
**Solution**:
1. Check session is cleared on logout
2. Check is_logged_in() function works
3. Verify @require_login decorator applied
4. Clear browser cookies

---

## Performance Tests

### Load Test
Generate multiple users and histories:
```python
from backend.database import *
from backend.auth import signup_user

# Create 10 test users
for i in range(10):
    email = f"test{i}@gmail.com"
    success, msg, user_id = signup_user(f"User {i}", email, f"Pass@{i}123")
    print(f"Created user {i}: {success}")
```

### Query Performance
```sql
-- Check indexes
PRAGMA index_list(users);
PRAGMA index_list(user_history);

-- Query performance
EXPLAIN QUERY PLAN SELECT * FROM user_history WHERE user_id = 1 ORDER BY timestamp DESC;
```

---

## Security Tests

### Test 1: SQL Injection
Try entering in signup form:
```
Email: test@gmail.com'; DROP TABLE users; --
```
**Expected**: Rejected as invalid email

### Test 2: XSS
Try entering in history metadata:
```
<script>alert('xss')</script>
```
**Expected**: Stored as text, not executed

### Test 3: CSRF
Try accessing API endpoints with GET instead of POST
**Expected**: No action taken

### Test 4: Session Hijacking
Try modifying session cookie
**Expected**: Signature validation fails

---

## Automated Testing (Optional)

Create `test_auth.py`:
```python
import unittest
from app import app
from backend.database import init_database, get_db
from backend.auth import signup_user, login_user

class TestAuthentication(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        init_database()
    
    def test_signup(self):
        response = self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'test@gmail.com',
            'password': 'Test@Pass123',
            'confirm_password': 'Test@Pass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_login(self):
        # First signup
        signup_user('Test User', 'test@gmail.com', 'Test@Pass123')
        
        # Verify user manually (skip email verification)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_verified = 1 WHERE email = 'test@gmail.com'")
            conn.commit()
        
        # Now login
        response = self.client.post('/login', data={
            'email': 'test@gmail.com',
            'password': 'Test@Pass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home

if __name__ == '__main__':
    unittest.main()
```

Run: `python -m unittest test_auth.py`

---

## Checklist for Full Testing

### Authentication Flow
- [ ] Signup with valid data
- [ ] Signup with invalid email
- [ ] Signup with weak password
- [ ] Signup with duplicate email
- [ ] Email verification works
- [ ] Email verification token expires
- [ ] Login with verified account
- [ ] Login with unverified account fails
- [ ] Login with wrong password fails
- [ ] Logout clears session

### Protected Routes
- [ ] Unlogged user redirected to login
- [ ] Logged user can access routes
- [ ] User context available in templates
- [ ] User data correct in templates

### History Tracking
- [ ] All activities logged
- [ ] Grouped by date correctly
- [ ] Delete item works
- [ ] Clear history works
- [ ] Only user's own history shown

### Password Reset
- [ ] Forgot password email sent
- [ ] Reset link works
- [ ] Token expires after 1 hour
- [ ] Password updated after reset
- [ ] Can login with new password

### Security
- [ ] Passwords hashed (not plaintext)
- [ ] Tokens signed and validated
- [ ] Session cookies HTTPOnly
- [ ] CSRF protection (if enabled)
- [ ] SQL injection prevented

---

**Status**: Ready for comprehensive testing
**Estimated Time**: 2-3 hours for full test coverage
