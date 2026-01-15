# CEFR English Level Test Platform - Technical Specification

**Version:** 1.0  
**Date:** 2025-12-12  
**Document Type:** Technical Specification for Development  
**Target Audience:** Development Team

---

## Executive Summary

This document provides a comprehensive technical specification for the CEFR English Level Test Platform, a web-based assessment system built with Streamlit. The platform enables students to take CEFR-aligned English proficiency tests and provides teachers with comprehensive dashboards for result management and analysis.

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Core Components](#4-core-components)
5. [Data Models](#5-data-models)
6. [User Interface Specifications](#6-user-interface-specifications)
7. [Business Logic](#7-business-logic)
8. [Security & Authentication](#8-security--authentication)
9. [Testing Requirements](#9-testing-requirements)
10. [Deployment Specifications](#10-deployment-specifications)
11. [Performance Requirements](#11-performance-requirements)
12. [Future Enhancements](#12-future-enhancements)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Client)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Student UI  │  │  Teacher UI  │  │  Report UI   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/WebSocket
┌──────────────────────────▼──────────────────────────────────┐
│              Streamlit Application Server                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │              Main Application (app.py)              │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐        │
│  │  Pages/    │  │   Utils/   │  │  Components/   │        │
│  │  - Student │  │  - CEFR    │  │  - Timer       │        │
│  │  - Teacher │  │  - DB Mgr  │  │  - Charts      │        │
│  │  - Reports │  │  - Data Mgr│  │  - Forms       │        │
│  └────────────┘  └────────────┘  └────────────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Data Layer                               │
│  ┌────────────────┐  ┌───────────────┐  ┌──────────────┐   │
│  │  SQLite DB     │  │  JSON Files   │  │  Secrets     │   │
│  │  (submissions) │  │  (questions)  │  │  (users)     │   │
│  └────────────────┘  └───────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Application Flow

```
User Access → Authentication → Role-Based Routing → 
  ├─ Student: Test Selection → Test Execution → Results
  └─ Teacher: Dashboard → Student Management → Reports
```

---

## 2. Technology Stack

### 2.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend Framework** | Streamlit | ≥1.27.0 | Web UI framework |
| **Backend Language** | Python | ≥3.8 | Application logic |
| **Data Processing** | Pandas | ≥1.5.0 | Data manipulation |
| **Visualization** | Plotly | ≥5.15.0 | Interactive charts |
| **Data Storage** | SQLite | 3.x | Database |
| **Session Management** | Streamlit Sessions | Built-in | State management |

### 2.2 Dependencies

```python
# requirements.txt
streamlit>=1.27.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
```

### 2.3 Design System

**EduPrompT v12.0 Design Tokens:**
- Primary: #FDFCFA (Background)
- Sage: #7BA38C (Success/Strengths)
- Coral: #E8785A (Alerts/Focus Areas)
- Sky: #6B9AC4 (Information)
- Gold: #C9A962 (Highlights)
- Fonts: 
  - Display: Cormorant Garamond
  - Mono: JetBrains Mono
  - Body: Sora

---

## 3. Project Structure

```
streamlit-lv-test/
│
├── app.py                              # Main application entry point
├── requirements.txt                    # Python dependencies
├── README.md                          # Project documentation
│
├── .streamlit/
│   ├── config.toml                    # Streamlit configuration
│   └── secrets.toml                   # User credentials (not in repo)
│
├── assets/
│   └── styles.css                     # Custom CSS styles
│
├── pages/
│   ├── 1_Student_Test.py              # Student test interface
│   ├── 2_Teacher_Dashboard.py         # Teacher management interface
│   └── 3_Reports.py                   # Report generation interface
│
├── utils/
│   ├── cefr_analyzer.py               # CEFR level analysis logic
│   ├── db_manager.py                  # Database operations
│   ├── data_manager.py                # Data import/export
│   ├── question_balancer.py           # Answer distribution logic
│   ├── visualization.py               # Chart generation
│   └── report_generator.py            # Premium HTML report generator
│
├── data/
│   └── submissions/                   # Student test submissions (SQLite)
│
├── tests/
│   └── test_balancer.py               # Unit tests
│
├── extracted_questions.json            # Question bank
└── extracted_questions_with_passages.json  # Questions with reading passages
```

---

## 4. Core Components

### 4.1 Authentication System (`app.py`)

**Function:** `login(username, password)`

```python
# Authentication Flow
1. Load user credentials from st.secrets['users']
2. Validate username and password
3. Set session state:
   - logged_in: True/False
   - user_role: 'student' or 'teacher'
   - student_info: {name, full_name, school, grade, class}
4. Redirect to role-based dashboard
```

**User Schema (secrets.toml):**
```toml
[users]
[users.username]
password = "hashed_password"
role = "student" | "teacher"
```

### 4.2 Student Test Module (`pages/1_Student_Test.py`)

**Key Features:**
- Test level selection (Pre-A1, A1, A2, B1, B2)
- Question shuffling (one-time at test start)
- Real-time timer
- Progress tracking
- Auto-save answers
- Immediate scoring

**Question Loading Logic:**
```python
def load_questions(level):
    """
    1. Load from JSON (extracted_questions.json)
    2. Validate question structure
    3. Connect passages to reading questions
    4. Return validated question list
    """
```

**Shuffle Logic:**
```python
def shuffle_options_once():
    """
    1. Executed once at test start
    2. Shuffle options for each question
    3. Update correct answer index
    4. Store in session state
    5. Maintain consistency throughout test
    """
```

**Answer Recording:**
- Student's answer stored as-is (no validation)
- Automatic progression to next question
- No answer changes allowed after submission
- Penalty for unanswered questions (-1 marker)

### 4.3 Teacher Dashboard (`pages/2_Teacher_Dashboard.py`)

**Features:**
- Student submission list
- Filtering by date, level, score
- Sortable columns
- Detailed view per student
- Export to CSV/Excel

**Data Display:**
```python
# Key Metrics
- Total Students
- Average Score
- Pass Rate
- Tests Completed Today
```

### 4.4 CEFR Analyzer (`utils/cefr_analyzer.py`)

**Purpose:** Analyze test results and provide CEFR level diagnosis

```python
class CEFRAnalyzer:
    def analyze_test_results(test_results):
        """
        Returns:
        {
            'current_cefr_level': str,
            'section_analysis': dict,
            'strengths': list,
            'weaknesses': list,
            'improvement_areas': list,
            'learning_curriculum': dict,
            'next_level_goal': dict
        }
        """
```

### 4.5 Premium Report Generator (`utils/report_generator.py`)

**Purpose:** Generate EduPrompT v12.0 styled HTML reports

```python
def generate_premium_report(student_info, test_results, analysis):
    """
    Generates single-file HTML with:
    - Interactive Chart.js visualizations
    - Radar chart (skill balance)
    - Doughnut chart (accuracy)
    - Personalized learning roadmap
    - Print-optimized layout
    """
```

### 4.6 Database Manager (`utils/db_manager.py`)

**Schema:**
```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT,
    school TEXT,
    grade TEXT,
    class TEXT,
    level TEXT NOT NULL,
    score INTEGER NOT NULL,
    correct INTEGER,
    total INTEGER,
    passed BOOLEAN,
    section_results TEXT,  -- JSON
    answers TEXT,          -- JSON
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Operations:**
- `save_submission(result)` - Save test result
- `get_student_submissions(student_id)` - Get student history
- `get_all_submissions()` - Get all results
- `get_submissions_by_level(level)` - Filter by level

---

## 5. Data Models

### 5.1 Question Model

```json
{
  "id": 1,
  "question": "Question text",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 0,  // Index of correct answer (0-3)
  "section": "Reading" | "Vocabulary" | "Grammar" | "Conversation",
  "passage": "Reading passage text (optional)"
}
```

### 5.2 Student Info Model

```json
{
  "name": "username",
  "full_name": "Full Name",
  "school": "School Name",
  "grade": "1" | "2" | "3",
  "class": "Class Name"
}
```

### 5.3 Test Result Model

```json
{
  "studentInfo": {...},
  "level": "Pre-A1" | "A1" | "A2" | "B1" | "B2",
  "submittedAt": "2025-12-12T10:30:00",
  "score": 85,
  "correct": 17,
  "total": 20,
  "passed": true,
  "sectionResults": {
    "Reading": {"correct": 5, "total": 8},
    "Grammar": {"correct": 8, "total": 10}
  },
  "answers": [0, 2, 1, ...]  // Student's answer indices
}
```

### 5.4 CEFR Analysis Model

```json
{
  "current_cefr_level": "A1",
  "section_analysis": {
    "Reading": {
      "correct": 5,
      "total": 8,
      "percentage": 62.5,
      "strength_level": "average"
    }
  },
  "strengths": ["List of strengths"],
  "weaknesses": ["List of weaknesses"],
  "improvement_areas": ["Prioritized improvement areas"],
  "learning_curriculum": {
    "priority_areas": [],
    "daily_practice": [],
    "materials": []
  },
  "next_level_goal": {
    "level": "A2",
    "target_score": 70,
    "estimated_duration": "3-6개월"
  }
}
```

---

## 6. User Interface Specifications

### 6.1 Main Page (`app.py`)

**Components:**
- Welcome message
- Login form (sidebar)
- Test account information
- CEFR level guide table
- Student/Teacher feature cards

**States:**
- Not logged in: Show welcome page + login
- Logged in (Student): Show student dashboard
- Logged in (Teacher): Show teacher dashboard

### 6.2 Student Dashboard

**Input Fields:**
- Student Information Form:
  - Full Name (required)
  - School Name
  - Grade (1/2/3)
  - Class
- Level Selection (Pre-A1 to B2)

**Actions:**
- Start Test (disabled if no student info)
- View Previous Results

### 6.3 Student Test Page

**Layout:**
- Sticky header with timer and progress
- Question display area
- Reading passage (if applicable)
- 4 option buttons
- Navigation controls
  - Previous Question
  - Emergency Submit
  - Next Question

**Timer:**
- Counts up from 00:00
- Displayed in MM:SS format
- Updates every second via JavaScript

**Progress Bar:**
- Visual indicator at header bottom
- Shows completion percentage

### 6.4 Test Results Page

**Tabs:**
1. **Results Summary**
   - Total score
   - CEFR level
   - Section breakdown
   - Time spent

2. **Premium Report** (NEW)
   - Download HTML button
   - Preview in expander
   - Includes interactive charts

3. **Counseling Report**
   - Markdown format
   - Downloadable
   - Detailed text analysis

4. **Learning Curriculum**
   - Study goals
   - Daily practice plan
   - Priorities
   - Recommended materials

### 6.5 Teacher Dashboard

**Metrics Cards:**
- Total Students
- Tests Submitted Today
- Average Score
- Pass Rate

**Data Table:**
- Sortable columns
- Filters:
  - Date range
  - Level
  - Pass/Fail status
  - Student name

**Actions:**
- View detailed result
- Export to CSV/Excel
- Generate reports

---

## 7. Business Logic

### 7.1 Question Distribution

**Answer Bias Prevention:**
- Questions loaded from JSON have answers at 0, 1, 2, 3 in sequence
- At test start, options are shuffled once per question
- Correct answer index updated accordingly
- Shuffled state stored in session
- Consistent throughout test session

### 7.2 Scoring Algorithm

```python
def calculate_score(answers, questions):
    """
    1. Compare each answer to correct index
    2. Count correct answers
    3. Apply penalty for unanswered (-1 marker)
    4. Penalty: -0.25 per unanswered question
    5. Calculate percentage: (correct - penalty) / total * 100
    6. Pass threshold: 70%
    """
```

### 7.3 CEFR Level Assignment

```python
Score Range → CEFR Level
90-100%  → Current level passed (advance)
70-89%   → Current level (borderline)
50-69%   → Current level (needs improvement)
<50%     → Below current level (remediation)
```

### 7.4 Section Analysis

```python
For each section:
  percentage = (correct / total) * 100
  
  if percentage >= 80: strength_level = "excellent"
  elif percentage >= 70: strength_level = "good"
  elif percentage >= 50: strength_level = "average"
  else: strength_level = "needs_improvement"
```

---

## 8. Security & Authentication

### 8.1 User Authentication

**Method:** Simple credential-based authentication using Streamlit secrets

**Implementation:**
```python
# .streamlit/secrets.toml (NOT in version control)
[users]
[users.student1]
password = "password123"
role = "student"

[users.teacher1]
password = "teacherpass"
role = "teacher"
```

**Security Considerations:**
- Secrets file excluded from git
- Passwords stored in plain text (for demo)
- **Production Recommendation:** 
  - Use bcrypt for password hashing
  - Implement proper authentication system
  - Use environment variables
  - Add session timeout

### 8.2 Role-Based Access Control

```python
# Student role can access:
- Student dashboard
- Test pages
- Personal results

# Teacher role can access:
- Teacher dashboard
- All student results
- Report generation
- Data export
```

### 8.3 Data Privacy

- Student data stored locally
- No external API calls
- Session data cleared on logout
- Submission data persists in database

---

## 9. Testing Requirements

### 9.1 Unit Tests

**Test Files:** `tests/test_balancer.py`

**Coverage:**
- Question loading functions
- Score calculation
- CEFR level assignment
- Data validation

### 9.2 Integration Tests

**Required Tests:**
- Complete test flow (login → test → results)
- Data persistence (save/load submissions)
- Report generation
- Export functionality

### 9.3 Manual Testing Checklist

```
□ Student can login
□ Student can fill information form
□ Test starts correctly
□ Questions display properly
□ Timer functions
□ Navigation works
□ Answers are saved
□ Scoring is accurate
□ Reports generate
□ Teacher can view results
□ Export works
```

---

## 10. Deployment Specifications

### 10.1 Local Deployment

```bash
# Requirements
- Python 3.8+
- pip
- Virtual environment (recommended)

# Steps
1. Clone repository
2. Create virtual environment: python -m venv venv
3. Activate: venv\Scripts\activate (Windows)
4. Install dependencies: pip install -r requirements.txt
5. Create secrets.toml in .streamlit/ folder
6. Run: streamlit run app.py
```

### 10.2 Streamlit Cloud Deployment

```yaml
# Configuration
Python version: 3.10
Main file: app.py
Requirements: requirements.txt

# Secrets (in Streamlit Cloud dashboard)
- Add users configuration
- Add any API keys if needed
```

### 10.3 Docker Deployment (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 11. Performance Requirements

### 11.1 Response Time

- Page load: < 2 seconds
- Question navigation: < 500ms
- Report generation: < 5 seconds
- Database queries: < 1 second

### 11.2 Scalability

**Current Limitations:**
- SQLite suitable for < 1000 concurrent users
- Session-based architecture

**Recommendations for Scale:**
- Migrate to PostgreSQL/MySQL
- Implement caching (Redis)
- Use load balancer
- Separate compute and storage

### 11.3 Browser Compatibility

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

---

## 12. Future Enhancements

### 12.1 Planned Features

1. **Advanced Analytics**
   - ML-based performance prediction
   - Trend analysis over time
   - Comparative analytics

2. **Enhanced Security**
   - OAuth integration
   - Password hashing
   - Session encryption
   - Rate limiting

3. **Content Management**
   - Admin panel for question management
   - Bulk import/export
   - Question versioning

4. **Communication**
   - Email notifications
   - Parent portal
   - Progress reports

5. **Mobile App**
   - React Native companion app
   - Offline test capability

### 12.2 Technical Debt

- Refactor authentication system
- Add comprehensive logging
- Implement proper error handling
- Add API documentation
- Create admin interface

---

## 13. Development Guidelines

### 13.1 Code Style

```python
# Follow PEP 8
# Use type hints
# Document functions with docstrings

def example_function(param: str) -> dict:
    """
    Brief description.
    
    Args:
        param: Description of parameter
        
    Returns:
        dict: Description of return value
    """
    pass
```

### 13.2 Git Workflow

```
main (production)
  └── develop (integration)
       ├── feature/student-dashboard
       ├── feature/teacher-reports
       └── bugfix/timer-issue
```

### 13.3 Naming Conventions

- **Files:** snake_case.py
- **Classes:** PascalCase
- **Functions:** snake_case()
- **Constants:** UPPER_SNAKE_CASE
- **Variables:** snake_case

---

## 14. API Reference (Internal)

### 14.1 CEFRAnalyzer

```python
class CEFRAnalyzer:
    def analyze_test_results(test_results: dict) -> dict:
        """Analyze test results and provide CEFR diagnosis"""
        
    def generate_counseling_report(analysis: dict) -> str:
        """Generate markdown counseling report"""
```

### 14.2 DatabaseManager

```python
class DatabaseManager:
    def __init__(db_path: str = "data/submissions.db"):
        """Initialize database connection"""
        
    def save_submission(result: dict) -> int:
        """Save test submission, returns submission_id"""
        
    def get_student_submissions(student_id: str) -> list:
        """Get all submissions for a student"""
        
    def get_all_submissions() -> list:
        """Get all submissions"""
```

### 14.3 ReportGenerator

```python
def generate_premium_report(
    student_info: dict,
    test_results: dict,
    analysis: dict
) -> str:
    """
    Generate EduPrompT v12.0 premium HTML report
    
    Returns:
        str: Complete HTML document with embedded CSS/JS
    """
```

---

## 15. Glossary

| Term | Definition |
|------|------------|
| CEFR | Common European Framework of Reference for Languages |
| Pre-A1 | Beginner level (before A1) |
| A1 | Elementary level |
| A2 | Pre-intermediate level |
| B1 | Intermediate level |
| B2 | Upper-intermediate level |
| EduPrompT | Design system name |
| Streamlit | Python web framework |

---

## 16. Contact & Support

**Project Lead:** Development Team  
**Documentation:** This file  
**Issue Tracking:** GitHub Issues  
**Updates:** Check STATUS_REPORT_*.md files

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-12 | System | Initial specification |

---

**End of Technical Specification Document**

This document should be treated as the single source of truth for reimplementing the CEFR English Level Test Platform. All features, data models, and business logic described herein must be faithfully reproduced in any new implementation.
