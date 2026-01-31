import requests
import json

# First, start a session to get a user_id
session = requests.Session()

# Make a request to set the session
resp = session.get('http://127.0.0.1:5000/')
print(f"Session established, status: {resp.status_code}")

# Now get the grouped history
resp = session.get('http://127.0.0.1:5000/api/history/grouped')
print(f"\nAPI Response Status: {resp.status_code}")

data = resp.json()
if data.get('success'):
    print("✓ API returned success")
    
    # Check if we have data
    history_data = data.get('data', {})
    
    for date_group, items in history_data.items():
        if items:
            print(f"\n{date_group}: {len(items)} items")
            
            # Show first item
            item = items[0]
            print(f"  - Type: {item.get('action_type')}")
            print(f"  - Title: {item.get('page_title')}")
            
            # Check metadata
            if item.get('metadata'):
                meta = item['metadata']
                if isinstance(meta, dict):
                    print(f"  - Metadata: {list(meta.keys())}")
                    if 'result' in meta:
                        print(f"  - Result stored: YES (length: {len(meta['result'])} chars)")
                else:
                    print(f"  - Metadata type: {type(meta)} (needs parsing!)")
else:
    print("✗ API returned error:", data.get('error'))
