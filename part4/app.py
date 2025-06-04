"""
Interview Preparation Web App - Main Application
A modular Streamlit-based application for practicing interview skills with AI assistance.
"""

import streamlit as st
from llm_provider import LLMProvider
from session_manager import SessionManager, initialize_session_state, handle_category_change
from ui_components import UIComponents, ChatInterface
from chat_handler import ChatHandler, MessageFormatter, ResponseValidator

# Page configuration
st.set_page_config(
    page_title="Interview Prep Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


class InterviewPrepApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize the application components."""
        # Initialize session state
        initialize_session_state()
        
        # Initialize core components
        self.session_manager = st.session_state.session_manager
        self.llm_provider = self._get_llm_provider()
        self.chat_handler = ChatHandler(self.llm_provider, self.session_manager)
        
        # Initialize UI components
        self.ui = UIComponents()
        self.chat_ui = ChatInterface()
        
        # Initialize formatters and validators
        self.formatter = MessageFormatter()
        self.validator = ResponseValidator()
    
    @st.cache_resource
    def _get_llm_provider(_self):
        """Initialize and cache the LLM provider."""
        return LLMProvider()
    
    def run(self):
        """Run the main application."""
        # Render main header
        self.ui.render_main_header()
        
        # Render sidebar and get UI state
        ui_state = self.ui.render_sidebar(self.session_manager, self.llm_provider)
        
        # Handle UI interactions
        self._handle_ui_interactions(ui_state)
        
        # Render main content
        self._render_main_content(ui_state)
        
        # Render footer
        self.ui.render_footer()
    
    def _handle_ui_interactions(self, ui_state):
        """Handle all UI interactions and state changes."""
        # Handle category change
        if ui_state['category'] != st.session_state.current_category:
            self.chat_handler.handle_category_change(ui_state['category'])
            st.rerun()
        
        # Handle clear chat
        if ui_state['clear_chat']:
            self.chat_handler.clear_chat()
            st.rerun()
        
        # Handle save session
        if ui_state['save_session']:
            if self.session_manager.save_current_session():
                self.ui.show_success_message("Session saved successfully!")
            else:
                self.ui.show_warning_message("No messages to save.")
    
    def _render_main_content(self, ui_state):
        """Render the main content area."""
        # Category information
        self.ui.render_category_info(st.session_state.current_category)
        
        # Chat messages
        chat_container = self.ui.render_chat_messages()
        
        # Handle user input
        self._handle_chat_input(ui_state, chat_container)
        
        # Quick suggestions (only if no messages)
        if not self.chat_handler.has_messages():
            self._handle_quick_suggestions(ui_state)
    
    def _handle_chat_input(self, ui_state, chat_container):
        """Handle chat input and AI response generation."""
        # Get user input
        user_input = self.chat_ui.get_user_input()
        
        if user_input:
            self._process_user_message(user_input, ui_state['temperature'], chat_container)
        
        # Handle suggested input from session state
        if hasattr(st.session_state, 'suggested_input'):
            suggested = st.session_state.suggested_input
            del st.session_state.suggested_input
            self._process_user_message(suggested, ui_state['temperature'], chat_container)
    
    def _process_user_message(self, message: str, temperature: float, chat_container):
        """Process a user message and generate AI response."""
        with chat_container:
            # Display user message
            self.chat_ui.display_user_message(message)
            
            # Generate and display AI response
            with self.chat_ui.display_thinking_spinner():
                success, response = self.chat_handler.process_user_input(message, temperature)
                
                if success:
                    # Validate and enhance response
                    is_valid, validation_error = self.validator.validate_response(response)
                    
                    if is_valid:
                        enhanced_response = self.validator.enhance_response(
                            response, st.session_state.current_category
                        )
                        formatted_response = self.formatter.format_ai_response(enhanced_response)
                        self.chat_ui.display_ai_message(formatted_response)
                    else:
                        error_msg = f"Response validation failed: {validation_error}"
                        self.chat_ui.display_error_message(error_msg)
                else:
                    # Display error message
                    self.ui.show_error_message(response)
            
            # Rerun to update the interface
            st.rerun()
    
    def _handle_quick_suggestions(self, ui_state):
        """Handle quick suggestion buttons."""
        suggestion = self.ui.render_quick_suggestions(st.session_state.current_category)
        
        if suggestion:
            # Store suggestion in session state for processing
            st.session_state.suggested_input = suggestion
            st.rerun()


def main():
    """Main application entry point."""
    try:
        app = InterviewPrepApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or check your configuration.")


if __name__ == "__main__":
    main() 