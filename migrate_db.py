
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_manager import DataManager
from utils.db_manager import DatabaseManager

def migrate_json_to_sqlite():
    print("Starting migration from JSON files to SQLite database...")
    
    # Initialize managers
    data_manager = DataManager()
    db_manager = DatabaseManager()
    
    # Load existing JSON submissions
    # Note: If existing JSONs are corrupted, DataManager might skip them or print errors.
    submissions = data_manager.load_submissions()
    
    if not submissions:
        print("No JSON submissions found to migrate.")
        return

    print(f"Found {len(submissions)} submissions. Migrating...")
    
    count = 0
    for sub in submissions:
        try:
            # Check for duplicates? For now, we just insert. 
            # Ideally we might check if filename exists in submission_data, 
            # but for a one-time migration to a fresh DB, simple insert is fine.
            db_manager.save_submission(sub)
            count += 1
        except Exception as e:
            print(f"Failed to migrate submission for {sub.get('studentInfo', {}).get('name')}: {e}")
            
    print(f"Migration complete. Successfully migrated {count}/{len(submissions)} records.")
    print(f"Database located at: {db_manager.db_path}")

if __name__ == "__main__":
    migrate_json_to_sqlite()
