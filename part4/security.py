"""
Security utilities for Interview Preparation App.
Includes input validation, sanitization, and basic security measures.
"""

import re
from typing import Tuple, List

# Security configuration
MAX_PROMPT_LENGTH = 5000
MAX_RESPONSE_LENGTH = 10000
BLOCKED_PATTERNS = [
    r'(?i)system\s*prompt',
    r'(?i)ignore\s+(previous|above|all)\s+instructions?',
    r'(?i)act\s+as\s+(?!interviewer|hr|recruiter|career\s+coach)',
    r'(?i)pretend\s+to\s+be',
    r'(?i)jailbreak',
    r'(?i)prompt\s+injection',
]

SENSITIVE_TERMS = [
    'api_key', 'password', 'secret', 'token', 'credential',
    'ssh', 'private_key', 'database', 'admin', 'root'
]


def validate_input_length(text: str, max_length: int = MAX_PROMPT_LENGTH) -> Tuple[bool, str]:
    """
    Validate that input text doesn't exceed maximum length.
    
    Args:
        text: Input text to validate
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(text) > max_length:
        return False, f"Input too long. Maximum {max_length} characters allowed."
    return True, ""


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful patterns.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potential HTML/XML tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove potential script tags (just in case)
    text = re.sub(r'(?i)<script.*?</script>', '', text)
    
    return text


def check_blocked_patterns(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains any blocked patterns.
    
    Args:
        text: Text to check
        
    Returns:
        Tuple of (contains_blocked_patterns, list_of_matches)
    """
    matches = []
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text):
            matches.append(pattern)
    
    return len(matches) > 0, matches


def check_sensitive_terms(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains sensitive terms that might indicate
    attempts to extract system information.
    
    Args:
        text: Text to check
        
    Returns:
        Tuple of (contains_sensitive_terms, list_of_matches)
    """
    matches = []
    text_lower = text.lower()
    
    for term in SENSITIVE_TERMS:
        if term in text_lower:
            matches.append(term)
    
    return len(matches) > 0, matches


def validate_interview_input(user_input: str) -> Tuple[bool, str]:
    """
    Comprehensive validation for interview preparation inputs.
    
    Args:
        user_input: User's input text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check length
    is_valid_length, length_error = validate_input_length(user_input)
    if not is_valid_length:
        return False, length_error
    
    # Check for blocked patterns
    has_blocked, blocked_patterns = check_blocked_patterns(user_input)
    if has_blocked:
        return False, "Input contains potentially harmful patterns. Please rephrase your question."
    
    # Check for sensitive terms (warning only, not blocking)
    has_sensitive, sensitive_terms = check_sensitive_terms(user_input)
    if has_sensitive:
        return False, f"Input contains sensitive terms: {', '.join(sensitive_terms)}. Please focus on interview-related topics."
    
    return True, ""


def sanitize_and_validate(user_input: str) -> Tuple[bool, str, str]:
    """
    Complete pipeline for sanitizing and validating user input.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Tuple of (is_valid, sanitized_input, error_message)
    """
    # First sanitize
    sanitized = sanitize_input(user_input)
    
    # Then validate
    is_valid, error_message = validate_interview_input(sanitized)
    
    return is_valid, sanitized, error_message


def log_security_event(event_type: str, details: str):
    """
    Log security events for monitoring purposes.
    In a production app, this would write to proper logging system.
    
    Args:
        event_type: Type of security event
        details: Event details
    """
    # For now, just print to console
    # In production, use proper logging
    print(f"[SECURITY] {event_type}: {details}")


def rate_limit_check(user_session_id: str) -> bool:
    """
    Basic rate limiting check.
    In a real app, this would use Redis or similar.
    
    Args:
        user_session_id: Session identifier
        
    Returns:
        True if request is allowed, False if rate limited
    """
    # For this demo, we'll always return True
    # In production, implement proper rate limiting
    return True 