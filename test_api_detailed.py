import requests
import json

# First, start a session to get a user_id
session = requests.Session()

# Make a request to set the session
resp = session.get('http://127.0.0.1:5000/')
print(f"Session established, status: {resp.status_code}")

# Now get the grouped history
resp = session.get('http://127.0.0.1:5000/api/history/grouped')
print(f"API Response Status: {resp.status_code}\n")

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
                            print(f"  - Metadata parsed: ✓ YES (type: dict)")
                            keys = list(meta.keys())
                            print(f"  - Metadata keys: {keys}")
                            if 'result' in meta:
                                result = meta['result']
                                print(f"  - Result found: ✓ YES ({len(result)} chars)")
                                print(f"  - Result preview: {result[:100]}...")
                            else:
                                print(f"  - Result found: ✗ NO")
                        else:
                            print(f"  - Metadata type: {type(meta).__name__} (NOT parsed!)")
                    else:
                        print(f"  - Metadata: None")
                    
                    break  # Show just one sample
            else:
                # Show any item if no generated output found
                item = items[0]
                print(f"\n  Sample {item.get('action_type')} record:")
                print(f"  - Title: {item.get('page_title')}")
                meta = item.get('metadata')
                print(f"  - Metadata type: {type(meta).__name__}")
else:
    print("✗ API returned error:", data.get('error'))
