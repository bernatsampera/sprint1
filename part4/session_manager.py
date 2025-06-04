"""
Session Management module for Interview Preparation App.
Handles session persistence, history, and state management.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st


class SessionManager:
    """Manages user sessions, history, and persistence."""
    
    def __init__(self, history_file: str = "session_history.json"):
        self.history_file = history_file
        self.max_sessions = 50  # Limit stored sessions
    
    def save_current_session(self) -> bool:
        """
        Save the current session to file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Load existing history
            all_history = self.load_all_sessions()
            
            # Add current session if it has messages
            if st.session_state.get("messages", []):
                session_data = {
                    "timestamp": datetime.now().isoformat(),
                    "category": st.session_state.get("current_category", "Unknown"),
                    "messages": st.session_state.messages.copy()
                }
                all_history.append(session_data)
                
                # Keep only last N sessions to prevent file from growing too large
                if len(all_history) > self.max_sessions:
                    all_history = all_history[-self.max_sessions:]
                
                # Save to file
                with open(self.history_file, 'w') as f:
                    json.dump(all_history, f, indent=2)
                
                return True
                
        except Exception as e:
            st.error(f"Failed to save session: {str(e)}")
            return False
        
        return False
    
    def load_all_sessions(self) -> List[Dict[str, Any]]:
        """
        Load all sessions from file.
        
        Returns:
            List of session dictionaries
        """
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            st.error(f"Failed to load session history: {str(e)}")
            return []
    
    def load_session(self, session_index: int) -> bool:
        """
        Load a specific session by index.
        
        Args:
            session_index: Index of session to load
            
        Returns:
            bool: True if loaded successfully
        """
        try:
            history = self.load_all_sessions()
            if 0 <= session_index < len(history):
                session = history[session_index]
                st.session_state.messages = session["messages"]
                st.session_state.current_category = session["category"]
                return True
        except Exception as e:
            st.error(f"Failed to load session: {str(e)}")
        
        return False
    
    def clear_current_session(self) -> None:
        """Clear the current session, optionally saving it first."""
        if st.session_state.get("messages", []):
            self.save_current_session()
        st.session_state.messages = []
    
    def delete_session(self, session_index: int) -> bool:
        """
        Delete a specific session from history.
        
        Args:
            session_index: Index of session to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            history = self.load_all_sessions()
            if 0 <= session_index < len(history):
                history.pop(session_index)
                with open(self.history_file, 'w') as f:
                    json.dump(history, f, indent=2)
                return True
        except Exception as e:
            st.error(f"Failed to delete session: {str(e)}")
        
        return False
    
    def get_session_summary(self, session: Dict[str, Any]) -> str:
        """
        Generate a summary string for a session.
        
        Args:
            session: Session dictionary
            
        Returns:
            str: Formatted summary
        """
        try:
            timestamp = datetime.fromisoformat(session["timestamp"]).strftime("%m/%d %H:%M")
            category = session["category"]
            message_count = len(session["messages"])
            
            # Get first user message as preview
            preview = ""
            for msg in session["messages"]:
                if msg["role"] == "user":
                    preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                    break
            
            return f"**{timestamp}** - {category} ({message_count} msgs)\n*{preview}*"
            
        except Exception:
            return "Invalid session data"
    
    def export_session(self, session_index: int, format: str = "json") -> Optional[str]:
        """
        Export a session in the specified format.
        
        Args:
            session_index: Index of session to export
            format: Export format ('json', 'text')
            
        Returns:
            str: Exported data or None if failed
        """
        try:
            history = self.load_all_sessions()
            if 0 <= session_index < len(history):
                session = history[session_index]
                
                if format == "json":
                    return json.dumps(session, indent=2)
                elif format == "text":
                    lines = [
                        f"Interview Session - {session['category']}",
                        f"Date: {session['timestamp']}",
                        "-" * 50
                    ]
                    
                    for msg in session["messages"]:
                        role = "You" if msg["role"] == "user" else "AI Assistant"
                        lines.append(f"\n{role}:")
                        lines.append(msg["content"])
                    
                    return "\n".join(lines)
                    
        except Exception as e:
            st.error(f"Failed to export session: {str(e)}")
        
        return None


def initialize_session_state():
    """Initialize all session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_category" not in st.session_state:
        st.session_state.current_category = "Behavioral Questions"
    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = None
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()


def handle_category_change(new_category: str):
    """Handle category change with session saving."""
    if new_category != st.session_state.current_category:
        # Save current session before switching
        if st.session_state.messages:
            st.session_state.session_manager.save_current_session()
            st.session_state.messages = []
        
        st.session_state.current_category = new_category 