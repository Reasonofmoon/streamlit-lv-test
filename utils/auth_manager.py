import os
import streamlit as st
from typing import Dict, Optional, List, Union

class AuthManager:
    """
    Normalize authentication across different environments (local, Vercel, etc.)
    """
    
    def __init__(self):
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """
        Load users from environment variables or Streamlit secrets
        Priority:
        1. Environment variables (Vercel/production)
        2. Streamlit secrets (local development)
        """
        users = {}
        
        # Try to load from environment variables first
        env_users = os.getenv('STREAMLIT_USERS')
        if env_users:
            try:
                import json
                users = json.loads(env_users)
            except:
                pass
        
        # Fall back to Streamlit secrets
        if not users and 'users' in st.secrets:
            users = dict(st.secrets['users'])
        
        return users
    
    def authenticate(self, username: str, password: str) -> Dict:
        """
        Authenticate user and return user info
        Returns empty dict if authentication fails
        """
        # Normalize input
        username = username.strip() if username else ""
        password = password.strip() if password else ""
        
        if not username or not password:
            return {}
        
        user = self.users.get(username)
        
        if user and user.get('password') == password:
            return {
                'username': username,
                'role': user.get('role', 'student'),
                'name': user.get('name', username),
                'school': user.get('school', ''),
                'grade': user.get('grade', ''),
                'class': user.get('class', '')
            }
        
        return {}
    
    def get_user_list(self) -> List[str]:
        """Get list of usernames (for debug purposes)"""
        return list(self.users.keys()) or []
    
    def add_user(self, username: str, password: str, role: str = 'student', **kwargs):
        """
        Add a new user
        This method is for testing/local development only
        """
        self.users[username] = {
            'password': password,
            'role': role,
            **kwargs
        }

def normalize_session_state():
    """
    Normalize session state to ensure all required keys exist
    """
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None
    
    if 'student_info' not in st.session_state:
        st.session_state['student_info'] = {}
    
    if 'test_completed' not in st.session_state:
        st.session_state['test_completed'] = False
    
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = None

def check_permission(required_role: Optional[str] = None) -> bool:
    """
    Check if current user has required permission
    If required_role is None, just check if logged in
    """
    if not st.session_state.get('logged_in', False):
        return False
    
    if required_role:
        return st.session_state.get('user_role') == required_role
    
    return True

def logout():
    """
    Clear session state for logout
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Re-initialize required session state
    normalize_session_state()
