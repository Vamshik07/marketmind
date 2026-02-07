#!/usr/bin/env python3
"""Create a test user for testing the MarketMind application"""

from backend.database import init_database, get_db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize database
init_database()

# Create test user
with get_db() as conn:
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute('SELECT id FROM users WHERE email = ?', ('ambativamshi743@gmail.com',))
    existing = cursor.fetchone()
    
    if existing:
        print('✓ Test user already exists!')
    else:
        # Create new user
        password_hash = generate_password_hash('TestPass@123')
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, is_verified, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test User', 'ambativamshi743@gmail.com', password_hash, 1, datetime.now(), datetime.now()))
        conn.commit()
        print('✓ Test user created successfully!')

# Verify user was created
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, is_verified FROM users WHERE email = ?', ('ambativamshi743@gmail.com',))
    user = cursor.fetchone()
    if user:
        print('\n' + '='*60)
        print('User Details:')
        print('='*60)
        print(f'  ID: {user[0]}')
        print(f'  Name: {user[1]}')
        print(f'  Email: {user[2]}')
        print(f'  Verified: {"Yes" if user[3] else "No"}')
        print('\n' + '='*60)
        print('Login Credentials:')
        print('='*60)
        print(f'  Email: ambativamshi743@gmail.com')
        print(f'  Password: TestPass@123')
        print('\n' + '='*60)
        print('✓ Ready to test!')
        print('='*60)
        print('\nGo to: http://127.0.0.1:5000/login')
        print('and login with the credentials above!')
