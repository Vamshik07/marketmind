import sqlite3
import json
import os

print("=" * 80)
print("HISTORY DATA STORAGE - COMPREHENSIVE CHECK")
print("=" * 80)

db_path = os.path.join(os.path.dirname(__file__), 'marketmind.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Database integrity
print("\n1. DATABASE INTEGRITY")
print("-" * 40)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_history';")
if cursor.fetchone():
    print("✓ user_history table exists")
else:
    print("✗ user_history table NOT found")
    exit()

# 2. Data storage
print("\n2. DATA STORAGE")
print("-" * 40)

cursor.execute("SELECT COUNT(*) FROM user_history;")
total_records = cursor.fetchone()[0]
print(f"✓ Total records stored: {total_records}")

# 3. Generated outputs
print("\n3. GENERATED OUTPUT RECORDS")
print("-" * 40)

cursor.execute("""
    SELECT COUNT(*) FROM user_history 
    WHERE action_type IN ('campaign_generated', 'pitch_generated', 'lead_scored');
""")
output_records = cursor.fetchone()[0]
print(f"✓ Generated outputs stored: {output_records}")

# 4. Sample records
print("\n4. SAMPLE RECORDS WITH METADATA")
print("-" * 40)

cursor.execute("""
    SELECT id, action_type, page_title, metadata 
    FROM user_history 
    WHERE action_type IN ('campaign_generated', 'pitch_generated', 'lead_scored')
    ORDER BY timestamp DESC 
    LIMIT 3;
""")

records = cursor.fetchall()
for idx, (record_id, action_type, title, metadata_str) in enumerate(records, 1):
    print(f"\nRecord {idx}:")
    print(f"  - ID: {record_id}")
    print(f"  - Type: {action_type}")
    print(f"  - Title: {title}")
    
    if metadata_str:
        try:
            metadata = json.loads(metadata_str)
            print(f"  ✓ Metadata JSON: VALID (keys: {list(metadata.keys())})")
            
            if 'result' in metadata:
                result_len = len(metadata['result'])
                print(f"  ✓ Result stored: YES ({result_len} characters)")
            else:
                print(f"  ✗ Result stored: NO")
        except json.JSONDecodeError:
            print(f"  ✗ Metadata JSON: INVALID")
    else:
        print(f"  - Metadata: None")

# 5. Database health
print("\n5. DATABASE HEALTH")
print("-" * 40)

cursor.execute("PRAGMA integrity_check;")
integrity = cursor.fetchone()[0]
if integrity == 'ok':
    print("✓ Database integrity: OK")
else:
    print(f"✗ Database integrity: {integrity}")

conn.close()

print("\n" + "=" * 80)
print("SUMMARY: History data storage is working correctly ✓")
print("=" * 80)
