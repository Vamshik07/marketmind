import sqlite3
import json
from datetime import datetime, timedelta
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'marketmind.db')

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize SQLite database with all required tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Users table - stores user account information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_verified BOOLEAN DEFAULT 0,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        ''')
        
        # Index for email lookups
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON users(email)')
        
        # User history table - tracks all user interactions and page visits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                page_url TEXT NOT NULL,
                page_title TEXT,
                action_type TEXT NOT NULL,
                metadata TEXT,
                timestamp DATETIME NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Index for fast queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON user_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON user_history(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_action_type ON user_history(action_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_timestamp ON user_history(user_id, timestamp DESC)')
        
        conn.commit()

def log_history_event(user_id, page_url, page_title, action_type, metadata=None, ip_address=None, user_agent=None):
    """Log a user action or page visit to history"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_history 
            (user_id, page_url, page_title, action_type, metadata, timestamp, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            page_url,
            page_title,
            action_type,
            json.dumps(metadata) if metadata else None,
            datetime.now().isoformat(),
            ip_address,
            user_agent
        ))
        conn.commit()
        return cursor.lastrowid

def get_user_history(user_id, limit=100, action_type=None):
    """Get user's history entries (most recent first)"""
    with get_db() as conn:
        cursor = conn.cursor()
        if action_type:
            cursor.execute('''
                SELECT * FROM user_history 
                WHERE user_id = ? AND action_type = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, action_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM user_history 
                WHERE user_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

def get_grouped_user_history(user_id, limit=500):
    """Get user's history grouped by date (Today, Yesterday, This week, Older)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_history 
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)
        
        grouped = {'Today': [], 'Yesterday': [], 'This week': [], 'Older': []}
        
        for row in rows:
            row_dict = dict(row)
            # Parse metadata from JSON string to dict
            if row_dict.get('metadata'):
                try:
                    row_dict['metadata'] = json.loads(row_dict['metadata'])
                except:
                    row_dict['metadata'] = {}
            timestamp = datetime.fromisoformat(row_dict['timestamp'])
            
            if timestamp >= today:
                grouped['Today'].append(row_dict)
            elif timestamp >= yesterday:
                grouped['Yesterday'].append(row_dict)
            elif timestamp >= week_ago:
                grouped['This week'].append(row_dict)
            else:
                grouped['Older'].append(row_dict)
        
        return grouped

def delete_history_item(user_id, history_id):
    """Delete a specific history item (with user verification)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_history WHERE id = ? AND user_id = ?', (history_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

def clear_user_history(user_id, action_type=None):
    """Clear all user history (optionally filtered by action type)"""
    with get_db() as conn:
        cursor = conn.cursor()
        if action_type:
            cursor.execute('DELETE FROM user_history WHERE user_id = ? AND action_type = ?', (user_id, action_type))
        else:
            cursor.execute('DELETE FROM user_history WHERE user_id = ?', (user_id,))
        conn.commit()

def delete_old_history(user_id, days=30):
    """Delete history older than specified days"""
    with get_db() as conn:
        cursor = conn.cursor()
        cutoff = datetime.now() - timedelta(days=days)
        cursor.execute('''
            DELETE FROM user_history 
            WHERE user_id = ? AND timestamp < ?
        ''', (user_id, cutoff.isoformat()))
        conn.commit()

def get_visit_history(user_id, limit=100):
    """Get page visit history (action_type = 'visit')"""
    return get_user_history(user_id, limit, action_type='visit')

def get_action_history(user_id, limit=100):
    """Get user action history (clicks, searches, etc)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_history 
            WHERE user_id = ? AND action_type IN ('click', 'search', 'submit', 'form_input')
            ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]


def save_campaign(product, audience, platform, result):
    """Save a campaign generation to history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO campaign_history (product, audience, platform, result)
        VALUES (?, ?, ?, ?)
    ''', (product, audience, platform, result))
    
    conn.commit()
    campaign_id = cursor.lastrowid
    conn.close()
    return campaign_id

def save_pitch(product, persona, result):
    """Save a pitch generation to history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO pitch_history (product, persona, result)
        VALUES (?, ?, ?)
    ''', (product, persona, result))
    
    conn.commit()
    pitch_id = cursor.lastrowid
    conn.close()
    return pitch_id

def save_lead(name, budget, need, urgency, result):
    """Save a lead scoring to history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO lead_history (name, budget, need, urgency, result)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, budget, need, urgency, result))
    
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id

def get_campaign_history(limit=50):
    """Retrieve campaign history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, product, audience, platform, result 
        FROM campaign_history 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'product': row[2],
            'audience': row[3],
            'platform': row[4],
            'result': row[5]
        })
    return history

def get_pitch_history(limit=50):
    """Retrieve pitch history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, product, persona, result 
        FROM pitch_history 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'product': row[2],
            'persona': row[3],
            'result': row[4]
        })
    return history

def get_lead_history(limit=50):
    """Retrieve lead history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, name, budget, need, urgency, result 
        FROM lead_history 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'name': row[2],
            'budget': row[3],
            'need': row[4],
            'urgency': row[5],
            'result': row[6]
        })
    return history

def delete_campaign(campaign_id):
    """Delete a campaign from history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM campaign_history WHERE id = ?', (campaign_id,))
    conn.commit()
    conn.close()

def delete_pitch(pitch_id):
    """Delete a pitch from history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pitch_history WHERE id = ?', (pitch_id,))
    conn.commit()
    conn.close()

def delete_lead(lead_id):
    """Delete a lead from history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lead_history WHERE id = ?', (lead_id,))
    conn.commit()
    conn.close()

def clear_all_history():
    """Clear all user history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM campaign_history')
    cursor.execute('DELETE FROM pitch_history')
    cursor.execute('DELETE FROM lead_history')
    conn.commit()
    conn.close()

def clear_campaign_history():
    """Clear only campaign history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM campaign_history')
    conn.commit()
    conn.close()

def clear_pitch_history():
    """Clear only pitch history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pitch_history')
    conn.commit()
    conn.close()

def clear_lead_history():
    """Clear only lead history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lead_history')
    conn.commit()
    conn.close()

def delete_campaigns_before(days=0, hours=0):
    """Delete campaigns older than specified time period"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Calculate cutoff time
    from datetime import datetime, timedelta
    cutoff_time = datetime.now() - timedelta(days=days, hours=hours)
    cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('DELETE FROM campaign_history WHERE timestamp < ?', (cutoff_str,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def delete_pitches_before(days=0, hours=0):
    """Delete pitches older than specified time period"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    from datetime import datetime, timedelta
    cutoff_time = datetime.now() - timedelta(days=days, hours=hours)
    cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('DELETE FROM pitch_history WHERE timestamp < ?', (cutoff_str,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def delete_leads_before(days=0, hours=0):
    """Delete leads older than specified time period"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    from datetime import datetime, timedelta
    cutoff_time = datetime.now() - timedelta(days=days, hours=hours)
    cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('DELETE FROM lead_history WHERE timestamp < ?', (cutoff_str,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def delete_campaign_by_date_range(start_date, end_date):
    """Delete campaigns within a specific date range"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM campaign_history WHERE timestamp BETWEEN ? AND ?',
        (start_date, end_date)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def delete_pitch_by_date_range(start_date, end_date):
    """Delete pitches within a specific date range"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM pitch_history WHERE timestamp BETWEEN ? AND ?',
        (start_date, end_date)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def delete_lead_by_date_range(start_date, end_date):
    """Delete leads within a specific date range"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM lead_history WHERE timestamp BETWEEN ? AND ?',
        (start_date, end_date)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def get_grouped_history():
    """Get all history grouped by date and type"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    def categorize_date(timestamp_str):
        """Categorize timestamp into date groups"""
        dt = datetime.strptime(timestamp_str[:19], '%Y-%m-%d %H:%M:%S').date()
        
        if dt == today:
            return 'Today'
        elif dt == yesterday:
            return 'Yesterday'
        elif dt >= week_ago:
            return 'This week'
        elif dt >= month_ago:
            return 'This month'
        else:
            return 'Earlier'
    
    grouped_data = {
        'Today': [],
        'Yesterday': [],
        'This week': [],
        'This month': [],
        'Earlier': []
    }
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get campaigns
    cursor.execute('''
        SELECT id, timestamp, product, audience, platform, result, 'campaign' as type
        FROM campaign_history 
        ORDER BY timestamp DESC
    ''')
    campaigns = cursor.fetchall()
    
    # Get pitches
    cursor.execute('''
        SELECT id, timestamp, product, persona, NULL, result, 'pitch' as type
        FROM pitch_history 
        ORDER BY timestamp DESC
    ''')
    pitches = cursor.fetchall()
    
    # Get leads
    cursor.execute('''
        SELECT id, timestamp, name, budget, need, result, 'lead' as type
        FROM lead_history 
        ORDER BY timestamp DESC
    ''')
    leads = cursor.fetchall()
    
    conn.close()
    
    # Combine and sort all items
    all_items = []
    
    for row in campaigns:
        all_items.append({
            'id': row[0],
            'timestamp': row[1],
            'type': 'campaign',
            'title': row[2],
            'meta': f"Audience: {row[3]} | Platform: {row[4]}",
            'result': row[5]
        })
    
    for row in pitches:
        all_items.append({
            'id': row[0],
            'timestamp': row[1],
            'type': 'pitch',
            'title': row[2],
            'meta': f"Persona: {row[3]}",
            'result': row[5]
        })
    
    for row in leads:
        all_items.append({
            'id': row[0],
            'timestamp': row[1],
            'type': 'lead',
            'title': row[2],
            'meta': f"Budget: {row[3]} | Need: {row[4]}",
            'result': row[5]
        })
    
    # Sort by timestamp descending
    all_items.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Group by date
    for item in all_items:
        date_group = categorize_date(item['timestamp'])
        grouped_data[date_group].append(item)
    
    return grouped_data

def get_grouped_campaign_history():
    """Get campaign history grouped by date"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    def categorize_date(timestamp_str):
        dt = datetime.strptime(timestamp_str[:19], '%Y-%m-%d %H:%M:%S').date()
        if dt == today:
            return 'Today'
        elif dt == yesterday:
            return 'Yesterday'
        elif dt >= week_ago:
            return 'This week'
        elif dt >= month_ago:
            return 'This month'
        else:
            return 'Earlier'
    
    grouped_data = {
        'Today': [],
        'Yesterday': [],
        'This week': [],
        'This month': [],
        'Earlier': []
    }
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, timestamp, product, audience, platform, result
        FROM campaign_history 
        ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        date_group = categorize_date(row[1])
        grouped_data[date_group].append({
            'id': row[0],
            'timestamp': row[1],
            'product': row[2],
            'audience': row[3],
            'platform': row[4],
            'result': row[5]
        })
    
    return grouped_data

def get_grouped_pitch_history():
    """Get pitch history grouped by date"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    def categorize_date(timestamp_str):
        dt = datetime.strptime(timestamp_str[:19], '%Y-%m-%d %H:%M:%S').date()
        if dt == today:
            return 'Today'
        elif dt == yesterday:
            return 'Yesterday'
        elif dt >= week_ago:
            return 'This week'
        elif dt >= month_ago:
            return 'This month'
        else:
            return 'Earlier'
    
    grouped_data = {
        'Today': [],
        'Yesterday': [],
        'This week': [],
        'This month': [],
        'Earlier': []
    }
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, timestamp, product, persona, result
        FROM pitch_history 
        ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        date_group = categorize_date(row[1])
        grouped_data[date_group].append({
            'id': row[0],
            'timestamp': row[1],
            'product': row[2],
            'persona': row[3],
            'result': row[4]
        })
    
    return grouped_data

def get_grouped_lead_history():
    """Get lead history grouped by date"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    def categorize_date(timestamp_str):
        dt = datetime.strptime(timestamp_str[:19], '%Y-%m-%d %H:%M:%S').date()
        if dt == today:
            return 'Today'
        elif dt == yesterday:
            return 'Yesterday'
        elif dt >= week_ago:
            return 'This week'
        elif dt >= month_ago:
            return 'This month'
        else:
            return 'Earlier'
    
    grouped_data = {
        'Today': [],
        'Yesterday': [],
        'This week': [],
        'This month': [],
        'Earlier': []
    }
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, timestamp, name, budget, need, urgency, result
        FROM lead_history 
        ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        date_group = categorize_date(row[1])
        grouped_data[date_group].append({
            'id': row[0],
            'timestamp': row[1],
            'name': row[2],
            'budget': row[3],
            'need': row[4],
            'urgency': row[5],
            'result': row[6]
        })
    
    return grouped_data

# ==================== USER MANAGEMENT FUNCTIONS ====================

def create_user(name, email, password_hash):
    """Create a new user account"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, is_verified, created_at, updated_at)
                VALUES (?, ?, ?, 0, ?, ?)
            ''', (name, email, password_hash, now, now))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Email already exists

def get_user_by_email(email):
    """Get user by email"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id):
    """Get user by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def verify_user_email(user_id):
    """Mark user email as verified"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET is_verified = 1, updated_at = ? WHERE id = ?',
            (datetime.now().isoformat(), user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def update_user_password(user_id, password_hash):
    """Update user password"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?',
            (password_hash, datetime.now().isoformat(), user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

# Initialize database on import
if not os.path.exists(DATABASE_PATH):
    init_database()

