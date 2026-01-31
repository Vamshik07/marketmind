"""
User activity history tracking module
Logs user actions for authenticated users only
"""

from datetime import datetime, timedelta
from backend.database import get_db
import json

def log_user_activity(user_id, page_url, page_title, action_type, metadata=None, ip_address=None, user_agent=None):
    """
    Log a user activity/action to history
    
    Args:
        user_id: Integer user ID (only for logged-in users)
        page_url: URL of the page
        page_title: Title of the page
        action_type: Type of action (login, logout, visit, click, form_submit, password_reset, etc.)
        metadata: Optional JSON metadata dict
        ip_address: User's IP address
        user_agent: User's browser user agent
    
    Returns:
        History record ID or None on error
    """
    if not user_id:
        return None
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
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
                datetime.utcnow().isoformat(),
                ip_address,
                user_agent
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            return None

def get_user_history(user_id, limit=500, action_type=None):
    """
    Get user's history entries
    
    Args:
        user_id: User ID
        limit: Maximum number of records
        action_type: Optional filter by action type
    
    Returns:
        List of history records
    """
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
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_grouped_user_history(user_id, limit=500):
    """
    Get user's history grouped by date (Today, Yesterday, This week, Older)
    
    Args:
        user_id: User ID
        limit: Maximum records per group
    
    Returns:
        Dictionary with date groups as keys
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_history 
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        now = datetime.utcnow()
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
            
            # Parse timestamp
            timestamp = datetime.fromisoformat(row_dict['timestamp'])
            
            # Group by date
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
    """
    Delete a specific history item (with user verification)
    
    Returns:
        True if deleted, False otherwise
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM user_history WHERE id = ? AND user_id = ?',
            (history_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def clear_user_history(user_id):
    """
    Clear all user history
    
    Returns:
        Number of deleted records
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_history WHERE user_id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount

def delete_old_history(user_id, days=90):
    """
    Delete history older than specified days
    
    Returns:
        Number of deleted records
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cutoff = datetime.utcnow() - timedelta(days=days)
        cursor.execute('''
            DELETE FROM user_history 
            WHERE user_id = ? AND timestamp < ?
        ''', (user_id, cutoff.isoformat()))
        conn.commit()
        return cursor.rowcount
