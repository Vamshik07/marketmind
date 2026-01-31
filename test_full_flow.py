import requests
import json

# Create a session
session = requests.Session()

# First, visit the home page to establish session
print("1. Establishing session...")
resp = session.get('http://127.0.0.1:5000/')
print(f"   Status: {resp.status_code}")

# Extract user_id from cookies if available
print("\n2. Visiting campaign page...")
resp = session.get('http://127.0.0.1:5000/campaign')
print(f"   Status: {resp.status_code}")

# Generate a campaign
print("\n3. Generating campaign...")
campaign_data = {
    'product': 'Test Widget',
    'audience': 'Developers',
    'platform': 'Twitter'
}

resp = session.post('http://127.0.0.1:5000/api/generate-campaign', json=campaign_data)
print(f"   Status: {resp.status_code}")

if resp.status_code == 200:
    result = resp.json()
    print(f"   Success: {result.get('success')}")
    if result.get('result'):
        print(f"   Result length: {len(result.get('result'))} chars")
        print(f"   Result preview: {result.get('result')[:100]}...")

# Now check if it's stored in history
print("\n4. Checking history...")
import time
time.sleep(1)  # Give it a second to write to DB

resp = session.get('http://127.0.0.1:5000/api/history/grouped')
print(f"   Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    if data.get('success'):
        history_data = data.get('data', {})
        total_items = sum(len(items) for items in history_data.values())
        print(f"   Total history items: {total_items}")
        
        # Find campaign_generated records
        for date_group, items in history_data.items():
            for item in items:
                if item.get('action_type') == 'campaign_generated':
                    print(f"\n   ✓ Found campaign_generated record!")
                    print(f"   - Type: {type(item.get('metadata'))}")
                    
                    meta = item.get('metadata')
                    if isinstance(meta, dict):
                        print(f"   ✓ Metadata is dict (properly parsed)")
                        print(f"   - Keys: {list(meta.keys())}")
                        
                        if 'result' in meta:
                            print(f"   ✓ Result stored: YES ({len(meta['result'])} chars)")
                            print(f"   - Preview: {meta['result'][:80]}...")
                        else:
                            print(f"   ✗ Result stored: NO")
                    else:
                        print(f"   ✗ Metadata is {type(meta).__name__} - NOT parsed!")
                    break
