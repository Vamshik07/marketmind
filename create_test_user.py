#!/usr/bin/env python3
"""Create a test user for testing the MarketMind application"""

from backend.database import init_database, get_db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize database
init_database()

# 🔹 PLACEHOLDERS (NO DEFAULT REAL DATA)
TEST_EMAIL = None
TEST_PASSWORD = None

if not TEST_EMAIL or not TEST_PASSWORD:
    print("⚠️ No default test email/password provided.")
    print("➡️ Skipping test user creation.")
    exit(0)

with get_db() as conn:
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id FROM users WHERE email = ?',
        (TEST_EMAIL,)
    )

    if cursor.fetchone():
        print('✓ Test user already exists!')
    else:
        cursor.execute("""
            INSERT INTO users
            (name, email, password_hash, is_verified, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Test User',
            TEST_EMAIL,
            generate_password_hash(TEST_PASSWORD),
            1,
            datetime.now(),
            datetime.now()
        ))

        conn.commit()
        print('✓ Test user created successfully!')
