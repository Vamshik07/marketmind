import requests
import json
import sqlite3

# Get a user_id from the database that has records
conn = sqlite3.connect('marketmind.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT user_id FROM user_history LIMIT 1")
user_id = cursor.fetchone()
if user_id:
    user_id = user_id[0]
else:
    print("No user_id found in database")
    exit()

conn.close()

print(f"Testing with user_id: {user_id}\n")

# Create a session and manually set the user_id in the session
session = requests.Session()

# First, get the home page to establish a session
resp = session.get('http://127.0.0.1:5000/')
print(f"Session established, status: {resp.status_code}")

# Extract session cookie
cookies = session.cookies
print(f"Cookies: {dict(cookies)}\n")

# Now manually test the API with this user by using query parameter or header
# Since we can't directly set session, let's test the grouped history directly
resp = session.get('http://127.0.0.1:5000/api/history/grouped')
print(f"API Response Status: {resp.status_code}\n")

try:
    data = resp.json()
    if data.get('success'):
        print("✓ API returned success")
        
        # Check if we have data
        history_data = data.get('data', {})
        
        total_items = sum(len(items) for items in history_data.values())
        print(f"Total items: {total_items}\n")
        
        for date_group, items in history_data.items():
            if items:
                print(f"{date_group}: {len(items)} items")
                
                # Show first generated output item
                for item in items:
                    if item.get('action_type') in ['campaign_generated', 'pitch_generated', 'lead_scored']:
                        print(f"\n  Sample {item.get('action_type')} record:")
                        print(f"  - Title: {item.get('page_title')}")
                        print(f"  - Timestamp: {item.get('timestamp')}")
                        
                        # Check metadata
                        meta = item.get('metadata')
                        if meta:
                            if isinstance(meta, dict):
                                print(f"  ✓ Metadata parsed correctly (type: dict)")
                                keys = list(meta.keys())
                                print(f"  - Keys: {keys}")
                                if 'result' in meta:
                                    result = meta['result']
                                    print(f"  ✓ Result found ({len(result)} chars)")
                                    print(f"  - Preview: {result[:80]}...")
                                else:
                                    print(f"  ✗ Result NOT found")
                            else:
                                print(f"  ✗ Metadata NOT parsed (type: {type(meta).__name__})")
                        else:
                            print(f"  - Metadata: None")
                        
                        break
    else:
        print("✗ API returned error:", data.get('error'))
except Exception as e:
    print(f"Error: {e}")
    print(f"Response text: {resp.text}")
