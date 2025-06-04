"""
UI Components module for Interview Preparation App.
Contains reusable Streamlit UI components and interface logic.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from system_prompts import PROMPT_MAPPING


class UIComponents:
    """Handles all UI components and interactions."""
    
    @staticmethod
    def render_sidebar(session_manager, llm_provider) -> Dict[str, Any]:
        """
        Render the sidebar with configuration and controls.
        
        Returns:
            Dict containing UI state values
        """
        ui_state = {}
        
        with st.sidebar:
            st.header("🔧 Configuration")
            
            # Display provider info
            provider_info = llm_provider.get_provider_info()
            
            if provider_info["provider"] == "openai":
                st.success(f"✅ Using OpenAI ({provider_info['model']})")
            else:
                if provider_info["available"]:
                    st.success(f"✅ Using Ollama ({provider_info['model']})")
                else:
                    st.error("❌ Ollama not available. Please start Ollama and ensure the model is installed.")
            
            # Interview category selection
            st.subheader("📝 Interview Category")
            ui_state['category'] = st.selectbox(
                "Choose your practice area:",
                options=list(PROMPT_MAPPING.keys()),
                index=list(PROMPT_MAPPING.keys()).index(st.session_state.current_category)
            )
            
            # Model settings
            st.subheader("⚙️ Model Settings")
            ui_state['temperature'] = st.slider(
                "Temperature (creativity level)",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Lower values make responses more focused and deterministic"
            )
            
            # Action buttons
            st.subheader("🎬 Actions")
            col1, col2 = st.columns(2)
            with col1:
                ui_state['clear_chat'] = st.button("🗑️ Clear Chat", type="secondary")
            
            with col2:
                ui_state['save_session'] = st.button("💾 Save Session", type="secondary")
            
            # Session history
            UIComponents.render_session_history(session_manager)
        
        return ui_state
    
    @staticmethod
    def render_session_history(session_manager):
        """Render the session history section in sidebar."""
        st.subheader("📚 Session History")
        history = session_manager.load_all_sessions()
        
        if history:
            with st.expander(f"📖 Past Sessions ({len(history)})", expanded=False):
                for i, session in enumerate(reversed(history[-10:])):  # Show last 10 sessions
                    session_summary = session_manager.get_session_summary(session)
                    st.markdown(session_summary)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Load", key=f"load_{i}"):
                            session_manager.load_session(len(history) - 1 - i)
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Delete", key=f"delete_{i}"):
                            session_manager.delete_session(len(history) - 1 - i)
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("No previous sessions found")
    
    @staticmethod
    def render_main_header():
        """Render the main application header."""
        st.title("🎯 Interview Preparation Assistant")
        st.markdown("Practice your interview skills with AI-powered assistance across different categories and question types.")
    
    @staticmethod
    def render_category_info(category: str):
        """Render information about the current category."""
        st.header(f"💬 {category} Practice")
        
        category_descriptions = {
            "Behavioral Questions": "Practice STAR method responses and common behavioral scenarios",
            "Technical Questions": "Sharpen your technical knowledge and problem-solving skills",
            "Job Description Analysis": "Analyze job postings and prepare targeted responses",
            "Final Interview Strategies": "Prepare for executive and final round interviews",
            "System Design": "Practice system design and architecture discussions"
        }
        
        st.info(f"📋 {category_descriptions.get(category, 'Practice interview skills')}")
    
    @staticmethod
    def render_chat_messages():
        """Render the chat message history."""
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        return chat_container
    
    @staticmethod
    def render_quick_suggestions(category: str) -> Optional[str]:
        """
        Render quick start suggestions for the current category.
        
        Returns:
            str: Selected suggestion or None
        """
        if st.session_state.messages:
            return None
            
        st.markdown("---")
        st.subheader("🚀 Quick Start Suggestions")
        
        suggestions = {
            "Behavioral Questions": [
                "Give me a behavioral question about teamwork",
                "Ask me about handling conflict at work",
                "Practice a question about leadership"
            ],
            "Technical Questions": [
                "Ask me a Python coding question",
                "Test my knowledge of system design",
                "Give me a JavaScript challenge"
            ],
            "Job Description Analysis": [
                "Help me analyze this job posting: [paste job description]",
                "What questions should I prepare for a Software Engineer role?",
                "How do I tailor my responses to this company?"
            ],
            "Final Interview Strategies": [
                "What questions should I ask the CEO?",
                "How do I discuss company culture fit?",
                "Practice salary negotiation scenarios"
            ],
            "System Design": [
                "Design a URL shortener like bit.ly",
                "How would you architect a chat application?",
                "Design a recommendation system"
            ]
        }
        
        current_suggestions = suggestions.get(category, [])
        
        cols = st.columns(len(current_suggestions))
        for i, suggestion in enumerate(current_suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}"):
                    return suggestion
        
        return None
    
    @staticmethod
    def render_footer():
        """Render the application footer."""
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.8em;'>
            Created by Bernat Sampera for Turing College Sprint 1
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    @staticmethod
    def show_success_message(message: str):
        """Show a success message."""
        st.success(message)
    
    @staticmethod
    def show_error_message(message: str):
        """Show an error message."""
        st.error(f"🚫 {message}")
    
    @staticmethod
    def show_warning_message(message: str):
        """Show a warning message."""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info_message(message: str):
        """Show an info message."""
        st.info(f"ℹ️ {message}")


class ChatInterface:
    """Handles chat-specific UI interactions."""
    
    @staticmethod
    def get_user_input() -> Optional[str]:
        """Get user input from chat interface."""
        return st.chat_input("Type your message or question here...")
    
    @staticmethod
    def display_thinking_spinner():
        """Display thinking spinner for AI response."""
        return st.spinner("Thinking...")
    
    @staticmethod
    def display_user_message(message: str):
        """Display a user message in chat."""
        with st.chat_message("user"):
            st.markdown(message)
    
    @staticmethod
    def display_ai_message(message: str):
        """Display an AI response in chat."""
        with st.chat_message("assistant"):
            st.markdown(message)
    
    @staticmethod
    def display_error_message(error_msg: str):
        """Display an error message in chat."""
        with st.chat_message("assistant"):
            st.error(error_msg) 