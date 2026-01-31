import sqlite3
import json
import os

db_path = os.path.join(os.path.dirname(__file__), 'marketmind.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get records with metadata (generated outputs)
cursor.execute("""
    SELECT id, user_id, page_title, action_type, metadata, timestamp 
    FROM user_history 
    WHERE action_type IN ('campaign_generated', 'pitch_generated', 'lead_scored')
    ORDER BY timestamp DESC 
    LIMIT 5;
""")

records = cursor.fetchall()
print(f"Found {len(records)} generated output records\n")

for record in records:
    record_id, user_id, title, action_type, metadata, timestamp = record
    print(f"ID: {record_id}")
    print(f"Type: {action_type}")
    print(f"Title: {title}")
    print(f"Timestamp: {timestamp}")
    
    if metadata:
        try:
            meta = json.loads(metadata)
            print(f"Metadata keys: {list(meta.keys())}")
            if 'result' in meta:
                print(f"Result stored: YES (length: {len(meta['result'])} chars)")
                print(f"Result preview: {meta['result'][:100]}...")
            else:
                print(f"Result stored: NO")
                print(f"Data: {meta}")
        except:
            print(f"Metadata: {metadata}")
    else:
        print("Metadata: None")
    
    print("-" * 80)

conn.close()
