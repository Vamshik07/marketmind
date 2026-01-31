# MarketMind - AI-Powered Marketing Platform with User Authentication

An intelligent sales and marketing platform powered by Groq's LLaMA AI model that generates marketing campaigns, crafts compelling pitches, and qualifies leads with advanced AI technology. Includes complete user authentication, email verification, password management, and activity history tracking.

## ✨ Key Features

### 🤖 AI Marketing Tools
1. **Campaign Generator**: Create data-driven marketing campaigns tailored to your product and audience
   - Campaign objectives, audience psychology, content ideas, ad copy variations, CTAs
   - Multiple platform support: LinkedIn, Facebook, Instagram, Twitter/X, YouTube, Email, TikTok, WhatsApp

2. **Sales Pitch Creator**: Craft personalized, compelling sales pitches for specific customer personas
   - 30-second elevator pitch, value proposition, differentiators, CTAs
   - AI-powered insights tailored to customer needs and pain points

3. **Lead Qualifier**: Identify and prioritize high-value leads using intelligent scoring
   - BANU-based evaluation: Budget, Authority, Need, Urgency
   - Qualification score (0-100), conversion probability, recommended next actions

### 🔐 User Authentication & Security
- **User Registration**: Secure signup with email verification
- **Email Verification**: Signed tokens with 24-hour expiry
- **Login/Logout**: Session-based authentication
- **Password Reset**: Time-limited reset tokens (1-hour expiry)
- **Password Security**: Strict validation rules, Werkzeug PBKDF2 hashing

### 📊 Activity History & Tracking
- **Automatic Activity Logging**: Track all user actions and tool usage
- **Grouped History Display**: Organized by date (Today, Yesterday, This week, Older)
- **Full Output Access**: View, copy, and download generated content
- **History Management**: Delete individual items or clear all history
- **Per-User Isolation**: Users see only their own history and data

## 📋 Project Structure

```
MarketMind/
├── app.py                              # Flask application with all routes
├── .env                               # Environment variables (API keys, email config)
├── marketmind.db                       # SQLite database
├── requirements.txt                    # Python dependencies
├── verify_system.py                    # System verification script
├── AUTH_SYSTEM_SETUP.md               # Authentication system setup guide
├── TESTING_GUIDE.md                    # Comprehensive testing guide
├── FEATURE_CHECKLIST.md               # Complete feature checklist
│
├── backend/
│   ├── __init__.py
│   ├── database.py                     # Database schema & operations
│   ├── auth.py                         # Authentication logic (signup, login, password reset)
│   ├── history.py                      # User activity tracking
│   ├── email_utils.py                  # Gmail SMTP email sending
│   ├── ai_engine.py                    # Groq API integration
│   └── prompts.py                      # AI prompt templates
│
└── frontend/
    ├── templates/
    │   ├── base.html                   # Base layout with navigation
    │   ├── index.html                  # Home page
    │   ├── campaign.html               # Campaign generator
    │   ├── pitch.html                  # Sales pitch generator
    │   ├── lead-score.html             # Lead scoring
    │   ├── history.html                # User activity history
    │   ├── signup.html                 # User registration
    │   ├── login.html                  # User login
    │   ├── forgot_password.html        # Password reset request
    │   ├── reset_password.html         # Password reset form
    │   ├── verification_pending.html   # Email verification pending
    │   ├── verify_success.html         # Email verification success
    │   ├── verify_error.html           # Email verification error
    │   ├── password_reset_sent.html    # Reset email sent confirmation
    │   ├── reset_password_success.html # Password reset success
    │   ├── reset_password_error.html   # Password reset error
    │   ├── 404.html                    # Not found error
    │   └── 500.html                    # Server error
    │
    ├── static/
    │   ├── css/
    │   │   ├── style.css               # Main styling
    │   │   └── modern.css              # Modern theme
    │   └── js/
    │       ├── main.js                 # Main JavaScript utilities
    │       └── modern.js               # Modern JavaScript
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Groq API Key (Get from https://console.groq.com)
- Gmail account with 2-Step Verification enabled

### Step 1: Install Dependencies

```bash
cd MarketMind
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root with:

```env
# AI Engine
GROQ_API_KEY=gsk_your_api_key_here

# Authentication & Security
SECRET_KEY=your-secret-key-change-in-production

# Email (Gmail SMTP for verification & password reset)
# Get App Password from: https://myaccount.google.com/apppasswords
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Application URL
APP_URL=http://127.0.0.1:5000
```

### Step 3: Verify System Configuration

```bash
python verify_system.py
```

This checks:
- ✅ All required files exist
- ✅ Python dependencies installed
- ✅ Environment variables configured
- ✅ Database connectivity
- ✅ Email configuration

### Step 4: Run the Application

```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## 🚀 Quick Start

1. **Visit home page**: http://127.0.0.1:5000
2. **Sign up**: Create account at /signup
3. **Verify email**: Click link in verification email
4. **Login**: Sign in with your credentials
5. **Generate content**: Use campaign, pitch, or lead scoring tools
6. **View history**: Access your activity history anytime

---

## 🌐 Usage Guide

### Authentication Flow

#### Sign Up
1. Click "Sign Up" on login page
2. Enter name, email, and password
3. Password must meet strict requirements:
   - More than 7 characters
   - At least 1 digit (0-9)
   - At least 1 special character (!, -, ))
   - Special character not at start/end
4. Check email for verification link
5. Click verification link (valid for 24 hours)
6. Email verified - ready to login

#### Login
1. Go to http://127.0.0.1:5000/login
2. Enter email and password
3. Email must be verified
4. Session created - access all features

#### Password Reset
1. On login page, click "Forgot Password?"
2. Enter registered email
3. Check email for reset link (valid for 1 hour)
4. Create new password (must meet requirements)
5. Login with new password

### Campaign Generator
1. From home, click "Campaign Generator"
2. Enter product description
3. Describe target audience
4. Select marketing platform(s)
5. Click "Generate Campaign"
6. View results with:
   - Campaign objectives
   - Audience psychology
   - Content ideas
   - Ad copy variations
   - CTAs
7. Copy results or download as text file

### Sales Pitch Creator
1. From home, click "Sales Pitch"
2. Enter product/solution name
3. Describe customer persona
4. Click "Generate Pitch"
5. Get personalized pitch with:
   - 30-second elevator pitch
   - Value proposition
   - Key differentiators
   - Recommended CTAs
6. Copy or download results

### Lead Qualifier
1. From home, click "Lead Scoring"
2. Enter lead information:
   - Lead name
   - Budget information
   - Business need
   - Urgency level
3. Click "Score Lead"
4. Get qualification with:
   - Qualification score (0-100)
   - Conversion probability
   - Recommended next actions
5. Save in history for reference

### Activity History
1. Click "History" in navigation (top-right)
2. Or click floating "History" button (bottom-right)
3. View all activities grouped by date
4. Expand items to see full details
5. **Copy output**: Click copy icon to clipboard
6. **Download**: Click download to save as text file
7. **Delete**: Remove individual items
8. **Clear all**: Delete entire history
9. **Only your data**: Each user sees only their own history

## 🔧 Technology Stack

- **Backend**: Flask 2.0+ (Python web framework)
- **Database**: SQLite3 with full schema (users, user_history)
- **Authentication**: Flask sessions (session-based, not Flask-Login)
- **Password Security**: Werkzeug PBKDF2 hashing
- **Token Management**: itsdangerous URLSafeTimedSerializer
- **Email Service**: Gmail SMTP (smtp.gmail.com:465)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Engine**: Groq API with LLaMA 3.1 8B Instant
- **HTTP Client**: Python Requests
- **Configuration**: python-dotenv for environment variables

## 📦 Dependencies

```
flask==3.0.0
groq==0.4.1
python-dotenv==1.0.0
werkzeug==3.0.0
itsdangerous==2.1.2
```

All dependencies listed in `requirements.txt`

## 🚀 Deployment

### Local Deployment
```bash
python app.py
```

### Production Deployment
Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔐 Environment Configuration

### API Key Setup
1. Visit https://console.groq.com
2. Sign up or login
3. Navigate to API keys section
4. Create new API key
5. Copy and store in `.env` file

## 📝 API Endpoints

### Authentication Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/signup` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | User logout |
| `/forgot-password` | GET/POST | Forgot password request |
| `/reset-password/<token>` | GET/POST | Reset password with token |
| `/verify/<token>` | GET | Email verification |
| `/verification-pending` | GET | Email verification pending page |

### Feature Routes (Protected - Require Login)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page |
| `/campaign` | GET | Campaign generator page |
| `/pitch` | GET | Sales pitch creator page |
| `/lead-score` | GET | Lead scoring page |
| `/history` | GET | User activity history |

### API Endpoints (Protected - Require Login)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate-campaign` | POST | Generate marketing campaign |
| `/api/generate-pitch` | POST | Generate sales pitch |
| `/api/score-lead` | POST | Score and qualify lead |
| `/api/history/grouped` | GET | Get grouped user history |
| `/api/history/delete/<id>` | DELETE | Delete history item |
| `/api/history/clear` | DELETE | Clear all user history |

### Request/Response Examples

#### Generate Campaign
**Request**:
```json
{
    "product": "AI Analytics Platform",
    "audience": "Marketing managers at mid-size e-commerce companies",
    "platform": "LinkedIn, Instagram"
}
```

**Response**:
```json
{
    "success": true,
    "campaign": "...generated campaign content...",
    "metadata": {
        "product": "AI Analytics Platform",
        "audience": "Marketing managers...",
        "platform": "LinkedIn, Instagram"
    }
}
```

#### Generate Pitch
**Request**:
```json
{
    "product": "Cloud-based inventory management system",
    "persona": "Operations Director at Fortune 500 retail company"
}
```

#### Score Lead
**Request**:
```json
{
    "name": "Sarah Johnson",
    "budget": "$150,000 annual software budget",
    "need": "Improving customer retention by 20%",
    "urgency": "Implementation needed by Q3, high priority"
}
```

#### Get History
**Response**:
```json
{
    "today": [
        {
            "id": 1,
            "action_type": "campaign_generated",
            "timestamp": "2024-01-31T14:30:00",
            "metadata": {...}
        }
    ],
    "yesterday": [...],
    "this_week": [...],
    "older": [...]
}
```

## 🐛 Troubleshooting

### Email Not Received
**Solution**:
1. Verify `.env` has correct GMAIL_ADDRESS
2. Check GMAIL_APP_PASSWORD is valid
3. Ensure Gmail 2-Step Verification is enabled
4. Confirm "Less secure apps" setting is OFF in Gmail
5. Check spam folder
6. Review Flask console for SMTP errors

### Login Issues
**Solution**:
1. Verify account email is verified (check inbox for verification link)
2. Confirm password is correct
3. Clear browser cookies
4. Ensure database exists: `marketmind.db`

### History Not Showing
**Solution**:
1. Verify you're logged in
2. Check user_id in database matches
3. Try different date filters
4. Clear browser cache

### Port 5000 Already in Use
```bash
# Change port in app.py
app.run(host='127.0.0.1', port=5001)
```

### Password Validation Errors
**Valid Password Example**: `MyPassword@123`

**Invalid Examples**:
- `password` - No digit or special character
- `Pass123` - No special character
- `!Password123` - Special character at start
- `Password123!` - Special character at end

---

## 📖 Documentation

Complete documentation available in:
- **[AUTH_SYSTEM_SETUP.md](AUTH_SYSTEM_SETUP.md)** - Complete authentication system setup and architecture
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing guide with all test scenarios
- **[FEATURE_CHECKLIST.md](FEATURE_CHECKLIST.md)** - Complete feature checklist and system status

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [Python Requests Library](https://docs.python-requests.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/security/)
- [itsdangerous Tokens](https://itsdangerous.palletsprojects.com/)
- [Gmail SMTP Configuration](https://support.google.com/accounts/answer/185833)
- [HTML/CSS/JavaScript Basics](https://developer.mozilla.org/)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review the documentation files (AUTH_SYSTEM_SETUP.md, TESTING_GUIDE.md)
3. Run `python verify_system.py` to check configuration
4. Check Flask console output for error messages

## 🎯 Roadmap

- [x] User authentication & profiles
- [x] Email verification workflow
- [x] Password reset functionality
- [x] User activity history tracking
- [x] Activity history display with copy/download
- [ ] Export campaign/pitch/lead-score results
- [ ] Multiple language support
- [ ] Advanced analytics dashboard
- [ ] CRM integration
- [ ] API rate limiting per user
- [ ] User settings and preferences
- [ ] Social login (Google, Microsoft)
- [ ] 2FA (Two-Factor Authentication)

---

## 🔐 Security

This system implements multiple security measures:
- ✅ Password hashing with Werkzeug PBKDF2
- ✅ Signed tokens for email verification
- ✅ Time-limited tokens (email: 24h, reset: 1h)
- ✅ Session-based authentication with HTTPOnly cookies
- ✅ Strict password validation
- ✅ Input validation and sanitization
- ✅ Cross-user data isolation
- ✅ OWASP Top 10 protection

## 🚀 Production Deployment

For production deployment:

1. **Update Configuration**:
   ```env
   SECRET_KEY=generate-strong-random-value
   SESSION_COOKIE_SECURE=True  # Requires HTTPS
   DEBUG=False
   ```

2. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Enable HTTPS**:
   - Use SSL certificate (Let's Encrypt recommended)
   - Redirect HTTP to HTTPS

4. **Database**:
   - Regular backups
   - Consider PostgreSQL for larger deployments
   - Monitor performance

5. **Monitoring**:
   - Set up error logging
   - Monitor API performance
   - Track authentication failures

---

**Built with ❤️ using Groq AI | Version 2.0.0 (with Authentication)**