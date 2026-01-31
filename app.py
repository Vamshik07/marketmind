from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import uuid
from datetime import timedelta
from dotenv import load_dotenv
from backend.ai_engine import generate_response
from backend.prompts import (
    campaign_prompt,
    sales_prompt,
    lead_scoring_prompt
)
from backend.database import (
    init_database,
    log_history_event,
    get_grouped_user_history,
    delete_history_item,
    clear_user_history,
    delete_old_history,
    get_user_by_id
)
from backend.auth import (
    signup_user,
    login_user,
    send_verification_email_to_user,
    verify_token,
    send_password_reset_email_to_user,
    reset_password
)
from backend.history import (
    log_user_activity,
    get_grouped_user_history as get_user_grouped_history,
    delete_history_item as delete_user_history_item,
    clear_user_history as clear_user_activity_history
)

load_dotenv()

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

# Initialize database on startup
init_database()

# ==================== HELPER FUNCTIONS ====================

def is_logged_in():
    """Check if user is logged in"""
    return 'logged_in_user_id' in session

def get_current_user():
    """Get current logged-in user"""
    if 'logged_in_user_id' not in session:
        return None
    return get_user_by_id(session['logged_in_user_id'])

def require_login(f):
    """Decorator to require authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        data = request.json or request.form
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', '')
        
        # Attempt signup
        success, message, user_id = signup_user(name, email, password, password_confirm)
        
        if not success:
            if request.is_json:
                return jsonify({'success': False, 'message': message}), 400
            return render_template('signup.html', error=message, name=name, email=email)
        
        # Send verification email
        app_url = os.getenv('APP_URL', 'http://127.0.0.1:5000')
        user = get_user_by_id(user_id)
        email_success, email_msg = send_verification_email_to_user(
            user_id, email, name, app_url
        )
        
        if not email_success:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Signup successful but email sending failed'}), 500
            return render_template('signup.html', 
                                 error='Signup successful but failed to send verification email. Please contact support.',
                                 name=name, email=email)
        
        # Redirect to verification pending page
        if request.is_json:
            return jsonify({'success': True, 'message': message}), 201
        return redirect(url_for('verification_pending', email=email))
    
    return render_template('signup.html')

@app.route('/verification-pending')
def verification_pending():
    """Show verification pending message"""
    email = request.args.get('email', '')
    return render_template('verification_pending.html', email=email)

@app.route('/verify/<token>')
def verify_email(token):
    """Verify email with token"""
    success, user_id, message = verify_token(token, 'email-verification')
    
    if not success:
        return render_template('verify_error.html', error=message), 400
    
    # Mark user as verified
    from backend.database import verify_user_email
    verify_user_email(user_id)
    
    return render_template('verify_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """User login"""
    if is_logged_in():
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        data = request.json or request.form
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Attempt login
        success, message, user_id = login_user(email, password)
        
        if not success:
            if request.is_json:
                return jsonify({'success': False, 'message': message}), 401
            return render_template('login.html', error=message, email=email)
        
        # Set session and log activity
        session['logged_in_user_id'] = user_id
        log_user_activity(
            user_id=user_id,
            page_url='/login',
            page_title='User Login',
            action_type='login',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        if request.is_json:
            return jsonify({'success': True, 'message': message}), 200
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    if is_logged_in():
        user_id = session.get('logged_in_user_id')
        log_user_activity(
            user_id=user_id,
            page_url='/logout',
            page_title='User Logout',
            action_type='logout',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
    
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password request"""
    if request.method == 'POST':
        data = request.json or request.form
        email = data.get('email', '').strip()
        
        app_url = os.getenv('APP_URL', 'http://127.0.0.1:5000')
        success, message = send_password_reset_email_to_user(email, app_url)
        
        if request.is_json:
            return jsonify({'success': success, 'message': message}), 200 if success else 400
        
        # Always show success message for security (don't reveal if email exists)
        return render_template('password_reset_sent.html', email=email)
    
    return render_template('forgot_password.html')

@app.route('/password-reset-sent')
def password_reset_sent():
    """Password reset email sent confirmation page"""
    return render_template('password_reset_sent.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_page(token):
    """Reset password with token"""
    if request.method == 'POST':
        data = request.json or request.form
        new_password = data.get('new_password', '')
        new_password_confirm = data.get('new_password_confirm', '')
        
        success, message = reset_password(token, new_password, new_password_confirm)
        
        if not success:
            if request.is_json:
                return jsonify({'success': False, 'message': message}), 400
            return render_template('reset_password.html', token=token, error=message)
        
        if request.is_json:
            return jsonify({'success': True, 'message': message}), 200
        return render_template('reset_password_success.html')
    
    # Verify token is valid before showing form
    success, user_id, message = verify_token(token, 'password-reset', max_age=3600)
    
    if not success:
        return render_template('reset_password_error.html', error=message), 400
    
    return render_template('reset_password.html', token=token)

@app.route('/reset-password-success')
def reset_password_success():
    """Password reset successful page"""
    return render_template('reset_password_success.html')

# ==================== EXISTING ROUTES ====================

@app.before_request
def before_request():
    """Middleware: Auto-track page visits and set up user session"""
    session.permanent = True
    
    # Create or retrieve user_id from session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    # Exclude static files and API endpoints for page visit tracking
    # Only track Campaign, Pitch, Lead Score, and History pages
    if not request.path.startswith('/static') and not request.path.startswith('/api'):
        # Only log visits to the 3 main feature pages + history
        pages_to_track = {
            '/campaign': 'Campaign Generator',
            '/pitch': 'Sales Pitch Generator',
            '/lead-score': 'Lead Qualifier',
            '/history': 'History'
        }
        
        if request.path in pages_to_track:
            page_title = pages_to_track[request.path]
            
            # Log page visit silently in background
            try:
                log_history_event(
                    user_id=user_id,
                    page_url=request.path,
                    page_title=page_title,
                    action_type='visit',
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent')
                )
            except Exception as e:
                print(f"History logging error: {e}")

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    if not is_logged_in():
        return redirect(url_for('login_page'))
    return render_template('index.html', user=get_current_user())

@app.route('/campaign')
@require_login
def campaign():
    """Campaign generator page"""
    return render_template('campaign.html', user=get_current_user())

@app.route('/pitch')
@require_login
def pitch():
    """Sales pitch generator page"""
    return render_template('pitch.html', user=get_current_user())

@app.route('/lead-score')
@require_login
def lead_score():
    """Lead scoring page"""
    return render_template('lead-score.html', user=get_current_user())

@app.route('/history')
@require_login
def history_page():
    """User activity history page"""
    return render_template('history.html', user=get_current_user())

# ==================== API ENDPOINTS ====================

@app.route('/api/generate-campaign', methods=['POST'])
def api_generate_campaign():
    """API endpoint to generate marketing campaign"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        data = request.json
        product = data.get('product', '')
        audience = data.get('audience', '')
        platform = data.get('platform', '')
        
        if not all([product, audience, platform]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        prompt = campaign_prompt(product, audience, platform)
        result = generate_response(prompt)
        
        # Log to user history
        log_user_activity(
            user_id=user_id,
            page_url=request.path,
            page_title='Campaign Generator',
            action_type='campaign_generated',
            metadata={'product': product, 'audience': audience, 'platform': platform, 'result': result},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pitch', methods=['POST'])
def api_generate_pitch():
    """API endpoint to generate sales pitch"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        data = request.json
        product = data.get('product', '')
        persona = data.get('persona', '')
        
        if not all([product, persona]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        prompt = sales_prompt(product, persona)
        result = generate_response(prompt)
        
        # Log to user history
        log_user_activity(
            user_id=user_id,
            page_url=request.path,
            page_title='Pitch Generator',
            action_type='pitch_generated',
            metadata={'product': product, 'persona': persona, 'result': result},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/score-lead', methods=['POST'])
def api_score_lead():
    """API endpoint to score leads"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        data = request.json
        name = data.get('name', '')
        budget = data.get('budget', '')
        need = data.get('need', '')
        urgency = data.get('urgency', '')
        
        if not all([name, budget, need, urgency]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        prompt = lead_scoring_prompt(name, budget, need, urgency)
        result = generate_response(prompt)
        
        # Log to user history
        log_user_activity(
            user_id=user_id,
            page_url=request.path,
            page_title='Lead Scorer',
            action_type='lead_scored',
            metadata={'name': name, 'budget': budget, 'need': need, 'urgency': urgency, 'result': result},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HISTORY API ENDPOINTS ====================

@app.route('/api/history/grouped', methods=['GET'])
def get_grouped_history():
    """Get current user's history grouped by date"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        history = get_user_grouped_history(user_id)
        return jsonify({'success': True, 'data': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/delete/<int:history_id>', methods=['DELETE'])
def delete_history_item(history_id):
    """Delete a specific history item"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        success = delete_user_history_item(user_id, history_id)
        
        if success:
            return jsonify({'success': True, 'message': 'History item deleted'})
        else:
            return jsonify({'error': 'History item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/clear', methods=['DELETE'])
def clear_all_history():
    """Clear all user history"""
    if not is_logged_in():
        return jsonify({'error': 'User not authenticated'}), 401
    
    try:
        user_id = session.get('logged_in_user_id')
        clear_user_activity_history(user_id)
        
        # Log this action
        log_user_activity(
            user_id=user_id,
            page_url='/api/history/clear',
            page_title='Clear History',
            action_type='history_cleared',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'success': True, 'message': 'All history cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

