import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'marketmind.db')
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")
    
    # Check if user_history table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_history';")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM user_history;")
        count = cursor.fetchone()[0]
        print(f"Records in user_history: {count}")
        
        # Show last 5 records
        cursor.execute("SELECT id, user_id, page_title, action_type, timestamp FROM user_history ORDER BY timestamp DESC LIMIT 5;")
        records = cursor.fetchall()
        print(f"\nLast 5 records:")
        for record in records:
            print(f"  ID: {record[0]}, User: {record[1]}, Title: {record[2]}, Type: {record[3]}, Time: {record[4]}")
    else:
        print("user_history table does not exist!")
    
    conn.close()
else:
    print("Database file does not exist!")
