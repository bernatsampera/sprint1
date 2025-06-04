"""
Chat Handler module for Interview Preparation App.
Manages chat interactions, message processing, and AI response coordination.
"""

import streamlit as st
from typing import Optional, Tuple
from system_prompts import get_system_prompt
from security import sanitize_and_validate, log_security_event


class ChatHandler:
    """Handles chat interactions and message processing."""
    
    def __init__(self, llm_provider, session_manager):
        self.llm_provider = llm_provider
        self.session_manager = session_manager
    
    def process_user_input(self, user_input: str, temperature: float = 0.7) -> Tuple[bool, str]:
        """
        Process user input through security validation and generate AI response.
        
        Args:
            user_input: Raw user input
            temperature: AI temperature setting
            
        Returns:
            Tuple of (success, message) - message is either AI response or error message
        """
        # Security validation
        is_valid, sanitized_input, error_message = sanitize_and_validate(user_input)
        
        if not is_valid:
            log_security_event(
                "INPUT_VALIDATION_FAILED", 
                f"Category: {st.session_state.current_category}, Error: {error_message}"
            )
            return False, f"Security Check Failed: {error_message}"
        
        # Add user message to session
        self.add_message("user", sanitized_input)
        
        # Generate AI response
        try:
            system_prompt = get_system_prompt(st.session_state.current_category)
            response = self.llm_provider.chat(
                system_prompt=system_prompt,
                user_prompt=sanitized_input,
                temperature=temperature
            )
            
            # Add AI response to session
            self.add_message("assistant", response)
            return True, response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.add_message("assistant", error_msg)
            log_security_event("AI_RESPONSE_ERROR", str(e))
            return False, error_msg
    
    def add_message(self, role: str, content: str):
        """Add a message to the current session."""
        st.session_state.messages.append({
            "role": role,
            "content": content
        })
    
    def process_suggestion(self, suggestion: str, temperature: float = 0.7) -> bool:
        """
        Process a quick suggestion as user input.
        
        Args:
            suggestion: The suggested prompt
            temperature: AI temperature setting
            
        Returns:
            bool: True if processed successfully
        """
        success, _ = self.process_user_input(suggestion, temperature)
        return success
    
    def clear_chat(self):
        """Clear the current chat session."""
        self.session_manager.clear_current_session()
    
    def handle_category_change(self, new_category: str):
        """
        Handle category change with proper session management.
        
        Args:
            new_category: The new category to switch to
        """
        if new_category != st.session_state.current_category:
            # Save current session before switching
            if st.session_state.messages:
                self.session_manager.save_current_session()
                st.session_state.messages = []
            
            st.session_state.current_category = new_category
    
    def get_chat_history(self) -> list:
        """Get the current chat history."""
        return st.session_state.get("messages", [])
    
    def has_messages(self) -> bool:
        """Check if there are any messages in the current session."""
        return len(st.session_state.get("messages", [])) > 0


class MessageFormatter:
    """Handles message formatting and display logic."""
    
    @staticmethod
    def format_ai_response(response: str) -> str:
        """
        Format AI response for display.
        
        Args:
            response: Raw AI response
            
        Returns:
            str: Formatted response
        """
        # Remove any excessive whitespace
        response = response.strip()
        
        # Ensure proper line breaks for readability
        if len(response) > 500:
            # Add spacing after periods for long responses
            response = response.replace(". ", ".\n\n")
        
        return response
    
    @staticmethod
    def format_user_message(message: str) -> str:
        """
        Format user message for display.
        
        Args:
            message: Raw user message
            
        Returns:
            str: Formatted message
        """
        return message.strip()
    
    @staticmethod
    def format_error_message(error: str) -> str:
        """
        Format error message for display.
        
        Args:
            error: Raw error message
            
        Returns:
            str: Formatted error message
        """
        return f"⚠️ {error}"
    
    @staticmethod
    def get_message_preview(message: str, max_length: int = 50) -> str:
        """
        Get a preview of a message for display in lists.
        
        Args:
            message: Full message content
            max_length: Maximum length of preview
            
        Returns:
            str: Truncated message preview
        """
        if len(message) <= max_length:
            return message
        
        return message[:max_length] + "..."


class ResponseValidator:
    """Validates AI responses for quality and safety."""
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, str]:
        """
        Validate AI response for quality and safety.
        
        Args:
            response: AI response to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if response is too short
        if len(response.strip()) < 10:
            return False, "Response too short"
        
        # Check if response is an error message
        if response.lower().startswith("error"):
            return False, "AI returned an error"
        
        # Check for inappropriate content patterns
        inappropriate_patterns = [
            "i cannot", "i can't help", "i'm not able",
            "that's inappropriate", "i shouldn't"
        ]
        
        response_lower = response.lower()
        for pattern in inappropriate_patterns:
            if pattern in response_lower:
                return False, f"AI declined to respond: {pattern}"
        
        return True, ""
    
    @staticmethod
    def enhance_response(response: str, category: str) -> str:
        """
        Enhance AI response based on category context.
        
        Args:
            response: Original AI response
            category: Interview category
            
        Returns:
            str: Enhanced response
        """
        # Add category-specific enhancements
        if category == "Behavioral Questions" and "star" not in response.lower():
            response += "\n\n💡 *Remember to use the STAR method: Situation, Task, Action, Result*"
        
        elif category == "Technical Questions" and len(response) < 100:
            response += "\n\n💡 *Feel free to ask follow-up questions for clarification*"
        
        elif category == "System Design" and "scalability" not in response.lower():
            response += "\n\n💡 *Consider discussing scalability, reliability, and performance*"
        
        return response 