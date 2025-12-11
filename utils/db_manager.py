
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "data/cefr_test.db"):
        self.db_path = db_path
        self.ensure_data_dir()
        self.init_db()

    def ensure_data_dir(self):
        """Ensure the directory for the database exists."""
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def init_db(self):
        """Initialize the database schema."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create submissions table
        # We store the core queryable fields as columns, and the full details in a JSON text column.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            level TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            passed BOOLEAN NOT NULL,
            submitted_at TIMESTAMP NOT NULL,
            submission_data TEXT NOT NULL
        )
        ''')
        
        # Create indexes for common queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_name ON submissions(student_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_level ON submissions(level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_submitted_at ON submissions(submitted_at)')
        
        conn.commit()
        conn.close()

    def connect(self):
        """Create a database connection."""
        return sqlite3.connect(self.db_path)

    def save_submission(self, submission_data: Dict[str, Any]) -> int:
        """
        Save a submission to the database.
        Returns the new submission ID.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Extract core fields
        student_name = submission_data.get('studentInfo', {}).get('name', 'Unknown')
        level = submission_data.get('level', 'Unknown')
        score = submission_data.get('score', 0)
        total = submission_data.get('total', 0)
        passed = submission_data.get('passed', False)
        
        # Use existing timestamp or current time
        submitted_at_str = submission_data.get('submittedAt')
        if not submitted_at_str:
            submitted_at = datetime.now()
        else:
            try:
                submitted_at = datetime.fromisoformat(submitted_at_str)
            except ValueError:
                submitted_at = datetime.now()
        
        # Make sure metadata is in the stored JSON
        submission_data['savedAt'] = datetime.now().isoformat()
        
        json_data = json.dumps(submission_data, ensure_ascii=False)

        cursor.execute('''
        INSERT INTO submissions (student_name, level, score, total_questions, passed, submitted_at, submission_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_name, level, score, total, passed, submitted_at, json_data))
        
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return new_id

    def load_submissions(self) -> List[Dict[str, Any]]:
        """
        Load all submissions, returning them as a list of dictionaries (mimicking strict JSON structure).
        """
        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT submission_data FROM submissions ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        
        submissions = []
        for row in rows:
            try:
                data = json.loads(row['submission_data'])
                submissions.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for submission: {e}")

        conn.close()
        return submissions

    def filter_submissions(self,
                          level: Optional[str] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          student_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Filter submissions using SQL queries for performance.
        """
        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT submission_data FROM submissions WHERE 1=1'
        params = []
        
        if level:
            query += ' AND level = ?'
            params.append(level)
            
        if student_name:
            query += ' AND student_name = ?'
            params.append(student_name)
            
        if start_date:
            query += ' AND submitted_at >= ?'
            params.append(start_date)
            
        if end_date:
            query += ' AND submitted_at <= ?'
            params.append(end_date)
            
        query += ' ORDER BY submitted_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        submissions = []
        for row in rows:
            try:
                data = json.loads(row['submission_data'])
                submissions.append(data)
            except json.JSONDecodeError:
                pass
                
        conn.close()
        return submissions

    def get_student_submissions(self, student_name: str) -> List[Dict[str, Any]]:
        return self.filter_submissions(student_name=student_name)

    def get_submissions_by_level(self, level: str) -> List[Dict[str, Any]]:
        return self.filter_submissions(level=level)

    def delete_all_submissions(self):
        """Clear all data. Useful for testing or resetting."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM submissions')
        conn.commit()
        conn.close()
