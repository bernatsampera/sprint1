# 🎯 Interview Preparation Assistant - Complete Project Guide

> **A comprehensive onboarding guide for developers and contributors**

Welcome to the Interview Preparation Assistant! This guide will help you understand the entire project architecture, design decisions, and implementation details. Whether you're a new contributor, code reviewer, or just curious about the implementation, this guide has you covered.

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Architecture & Design Philosophy](#-architecture--design-philosophy)
3. [Module Deep Dive](#-module-deep-dive)
4. [AI Prompting Strategy](#-ai-prompting-strategy)
5. [Data Flow & State Management](#-data-flow--state-management)
6. [Security & Validation](#-security--validation)
7. [Configuration & Environment](#-configuration--environment)
8. [Development Workflow](#-development-workflow)
9. [Testing & Debugging](#-testing--debugging)
10. [Extending the Application](#-extending-the-application)

---

## 🚀 Project Overview

### What is this application?

The Interview Preparation Assistant is a **modular, AI-powered Streamlit web application** designed to help job seekers practice different types of interviews. It combines multiple AI prompting techniques with a clean, maintainable codebase.

### Key Features

- **5 Interview Categories**: Behavioral, Technical, Job Analysis, Final Interview, System Design
- **Dual AI Backend**: OpenAI (premium) + Ollama (local/free) with automatic fallback
- **Smart Prompting**: 5 different AI prompting techniques optimized for each interview type
- **Session Management**: Save, load, export, and organize practice sessions
- **Security Layer**: Input validation, sanitization, and prompt injection protection
- **Modular Architecture**: Clean separation of concerns for maintainability

### Technology Stack

```
Frontend:     Streamlit (Python web framework)
AI Backends:  OpenAI API + Ollama (local LLM)
HTTP Client:  httpx (async HTTP with timeout handling)
Dependencies: uv (modern Python package manager)
Data Format:  JSON (session persistence)
Security:     Custom validation + regex patterns
```

---

## 🏗️ Architecture & Design Philosophy

### Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Fail Gracefully**: Robust error handling and user-friendly messaging
3. **Configurability**: Easy to switch between AI providers and adjust settings
4. **Extensibility**: Simple to add new interview categories or prompting techniques
5. **Security First**: Multiple layers of input validation and sanitization

### Modular Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        app.py                               │
│                   (Main Controller)                         │
│  • Orchestrates all components                              │
│  • Handles application flow                                 │
│  • Manages UI state transitions                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
┌────────▼──────┐ ┌────────▼──────┐
│ UI Components │ │ Chat Handler  │
│               │ │               │
│ • Sidebar     │ │ • Message     │
│ • Chat UI     │ │   Processing  │
│ • Suggestions │ │ • AI Response │
│ • History     │ │ • Validation  │
└───────┬───────┘ └───────┬───────┘
        │                 │
        │        ┌────────▼──────┐
        │        │ LLM Provider  │
        │        │               │
        │        │ • OpenAI      │
        │        │ • Ollama      │
        │        │ • Timeouts    │
        │        │ • Retry Logic │
        │        └───────┬───────┘
        │                │
┌───────▼───────┐ ┌──────▼───────┐
│ Session Mgmt  │ │ System       │
│               │ │ Prompts      │
│ • Save/Load   │ │              │
│ • History     │ │ • 5 Prompt   │
│ • Export      │ │   Techniques │
│ • Cleanup     │ │ • Metadata   │
└───────────────┘ └──────────────┘
        │
┌───────▼───────┐
│ Security      │
│               │
│ • Validation  │
│ • Sanitization│
│ • Logging     │
└───────────────┘
```

---

## 📦 Module Deep Dive

### 1. `app.py` - Main Application Controller

**Purpose**: Orchestrates all components and manages application flow

**Key Classes:**

- `InterviewPrepApp`: Main application controller

**Responsibilities:**

- Initialize all components
- Handle UI state changes
- Coordinate between modules
- Error handling and recovery

**Key Methods:**

```python
def run(self):                    # Main application loop
def _handle_ui_interactions(self): # Process UI events
def _render_main_content(self):   # Display main interface
def _process_user_message(self):  # Handle chat interactions
```

### 2. `llm_provider.py` - AI Backend Management

**Purpose**: Unified interface for different AI providers with robust error handling

**Key Classes:**

- `LLMProvider`: Manages OpenAI and Ollama backends

**Key Features:**

- **Automatic Detection**: Detects available AI backend based on configuration
- **Timeout Management**: Configurable timeouts for different operations
- **Retry Logic**: Exponential backoff for failed requests
- **Resource Cleanup**: Proper connection management

**Configuration:**

```python
# Timeout settings
timeout = httpx.Timeout(
    connect=10.0,   # Connection timeout
    read=120.0,     # Read timeout for responses
    write=30.0,     # Write timeout
    pool=180.0      # Pool timeout
)
```

### 3. `session_manager.py` - Session Persistence

**Purpose**: Manages user sessions, history, and data persistence

**Key Classes:**

- `SessionManager`: Core session management

**Features:**

- **Auto-save**: Sessions saved when switching categories
- **History Management**: Load, delete, and organize past sessions
- **Export Functionality**: Export sessions in JSON or text format
- **Data Integrity**: Error handling for corrupted session files

**File Structure:**

```json
{
  "timestamp": "2024-06-04T11:34:52.123456",
  "category": "Behavioral Questions",
  "messages": [
    {"role": "user", "content": "Give me a behavioral question"},
    {"role": "assistant", "content": "Tell me about a time..."}
  ]
}
```

### 4. `ui_components.py` - Streamlit UI Components

**Purpose**: Reusable UI components and interface logic

**Key Classes:**

- `UIComponents`: Sidebar, chat, suggestions, etc.
- `ChatInterface`: Chat-specific UI interactions

**Components:**

- **Sidebar**: Configuration, model settings, session history
- **Chat Interface**: Message display and input handling
- **Quick Suggestions**: Category-specific starter prompts
- **Status Messages**: Success, error, and warning notifications

### 5. `chat_handler.py` - Chat Logic Management

**Purpose**: Processes chat interactions and coordinates AI responses

**Key Classes:**

- `ChatHandler`: Main chat coordination
- `MessageFormatter`: Message formatting and display
- `ResponseValidator`: AI response quality checks

**Workflow:**

```
User Input → Security Validation → AI Processing → Response Enhancement → Display
```

### 6. `system_prompts.py` - AI Prompting Strategies

**Purpose**: Implements different prompting techniques optimized for each interview type

**Prompting Techniques:**

1. **Few-shot Learning** → Behavioral Questions
2. **Zero-shot** → Technical Questions
3. **Chain-of-thought** → Job Description Analysis
4. **Role Prompting** → Final Interview Strategies
5. **Instruction-based** → System Design

### 7. `security.py` - Security & Validation

**Purpose**: Input validation, sanitization, and security measures

**Security Layers:**

- **Length Validation**: Prevents overly long inputs
- **Pattern Blocking**: Detects prompt injection attempts
- **Content Sanitization**: Removes HTML/script tags
- **Sensitive Term Detection**: Blocks inappropriate content

---

## 🧠 AI Prompting Strategy

### The Science Behind the Mapping

Each interview category is paired with the most effective prompting technique based on cognitive psychology and learning theory:

#### 1. **Behavioral Questions → Few-shot Learning**

```python
BEHAVIORAL_FEW_SHOT = """
You are an experienced HR interviewer...

Example 1:
Question: "Tell me about a time when..."
Good Answer: "In my previous role, I worked with..."
Feedback: "Excellent! You showed empathy..."
```

**Why this works:**

- **Pattern Recognition**: Shows candidates the STAR method structure
- **Quality Examples**: Demonstrates what good answers look like
- **Immediate Feedback**: Helps calibrate response quality
- **Scaffolding**: Provides support structure for complex responses

#### 2. **Technical Questions → Zero-shot**

```python
TECHNICAL_ZERO_SHOT = """
You are a senior software engineer...
Ask clear, relevant technical questions...
Evaluate responses for technical accuracy...
```

**Why this works:**

- **Authentic Assessment**: Tests genuine knowledge without hints
- **Real Conditions**: Mirrors actual technical interviews
- **Unbiased Evaluation**: No examples to skew responses
- **Skill Discovery**: Reveals true technical competency

#### 3. **Job Description Analysis → Chain-of-thought**

```python
JOB_ANALYSIS_COT = """
Follow this step-by-step approach:
Step 1: Identify key requirements...
Step 2: Categorize into "Must-have" vs "Nice-to-have"...
Step 3: Identify potential interview questions...
```

**Why this works:**

- **Systematic Decomposition**: Breaks complex analysis into steps
- **Cognitive Load Management**: Prevents overwhelm
- **Complete Coverage**: Ensures no important aspects are missed
- **Transferable Framework**: Teaches reusable analysis skills

#### 4. **Final Interview → Role Prompting**

```python
FINAL_INTERVIEW_ROLE = """
You are the CEO/Hiring Manager...
Your personality:
- Thoughtful and strategic
- Interested in motivations...
```

**Why this works:**

- **Contextual Immersion**: Creates realistic executive interaction
- **Authentic Dynamics**: Simulates real power structures
- **Strategic Focus**: Emphasizes high-level thinking
- **Bidirectional Evaluation**: Reminds candidates they're evaluating too

#### 5. **System Design → Instruction-based**

```python
SYSTEM_DESIGN_INSTRUCTION = """
Follow these specific instructions:
1. Start with clarifying questions...
2. Guide through capacity estimation...
3. Ask about high-level architecture...
```

**Why this works:**

- **Structured Framework**: Provides roadmap for complex problems
- **Comprehensive Coverage**: Ensures all design aspects are addressed
- **Industry Standard**: Mirrors real system design interview format
- **Confidence Building**: Gives candidates a clear process to follow

### Metadata and Configuration

Each prompt includes metadata for better understanding:

```python
PROMPT_METADATA = {
    "BEHAVIORAL_FEW_SHOT": {
        "technique": "Few-shot Learning",
        "cognitive_principle": "Pattern Recognition & Modeling",
        "best_for": "Skill demonstration through examples",
        "learning_outcome": "Understanding of expected response structure"
    }
    # ... more metadata
}
```

---

## 📊 Data Flow & State Management

### Streamlit Session State

The application uses Streamlit's session state for persistence:

```python
# Core state variables
st.session_state.messages = []              # Current chat history
st.session_state.current_category = ""      # Active interview category
st.session_state.llm_provider = None        # AI provider instance
st.session_state.session_manager = None     # Session manager instance
```

### Data Flow Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ User Input  │───▶│  Security    │───▶│ Chat        │
│             │    │  Validation  │    │ Handler     │
└─────────────┘    └──────────────┘    └─────┬───────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌─────▼───────┐
│ UI Display  │◀───│  Response    │◀───│ LLM         │
│             │    │  Formatting  │    │ Provider    │
└─────────────┘    └──────────────┘    └─────────────┘
        │
        ▼
┌─────────────┐
│ Session     │
│ Storage     │
└─────────────┘
```

### Message Flow

1. **User Input**: Message entered via Streamlit chat input
2. **Security Check**: Validation and sanitization
3. **AI Processing**: Sent to appropriate AI provider
4. **Response Enhancement**: Category-specific improvements
5. **Display**: Formatted and shown to user
6. **Storage**: Added to session history

---

## 🔒 Security & Validation

### Multi-layer Security Approach

#### Layer 1: Input Length Validation

```python
MAX_PROMPT_LENGTH = 5000
if len(text) > max_length:
    return False, f"Input too long. Maximum {max_length} characters allowed."
```

#### Layer 2: Pattern Blocking

```python
BLOCKED_PATTERNS = [
    r'(?i)system\s*prompt',
    r'(?i)ignore\s+(previous|above|all)\s+instructions?',
    r'(?i)jailbreak',
    r'(?i)prompt\s+injection',
]
```

#### Layer 3: Content Sanitization

```python
def sanitize_input(text: str) -> str:
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove HTML/XML tags
    text = re.sub(r'<[^>]*>', '', text)
    return text
```

#### Layer 4: Sensitive Term Detection

```python
SENSITIVE_TERMS = [
    'api_key', 'password', 'secret', 'token', 'credential',
    'ssh', 'private_key', 'database', 'admin', 'root'
]
```

### Security Event Logging

All security events are logged for monitoring:

```python
def log_security_event(event_type: str, details: str):
    print(f"[SECURITY] {event_type}: {details}")
    # In production, use proper logging infrastructure
```

---

## ⚙️ Configuration & Environment

### Environment Variables

```bash
# .env file configuration
OPENAI_API_KEY=your_openai_api_key_here  # Optional: Use OpenAI
OLLAMA_BASE_URL=http://localhost:11434   # Ollama server URL
OLLAMA_MODEL=gemma2:4b                   # Local model name
```

### Provider Selection Logic

```python
def __init__(self):
    # Check for OpenAI key first
    if self.openai_api_key and self.openai_api_key.strip():
        self.provider = "openai"
        self._init_openai()
    else:
        # Fall back to Ollama
        self.provider = "ollama"
        self._init_ollama()
```

### Timeout Configuration

```python
# Ollama timeout settings
timeout = httpx.Timeout(
    connect=10.0,   # Initial connection
    read=120.0,     # AI response generation
    write=30.0,     # Request writing
    pool=180.0      # Total pool timeout
)
```

---

## 💻 Development Workflow

### Setting Up Development Environment

1. **Install Dependencies**:

   ```bash
   cd part4
   uv sync  # Install all dependencies
   ```

2. **Configure Environment**:

   ```bash
   # Edit .env file
   OPENAI_API_KEY=your_key_here  # Optional
   ```

3. **Start Ollama** (if not using OpenAI):

   ```bash
   ollama serve
   ollama pull gemma2:4b
   ```

4. **Run Application**:
   ```bash
   uv run streamlit run app.py
   ```

### Code Quality Standards

- **Type Hints**: All functions should include proper type annotations
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Error Handling**: Graceful failure handling with user-friendly messages
- **Separation of Concerns**: Each module should have a single responsibility

### Adding New Features

#### Adding a New Interview Category

1. **Add Prompt** in `system_prompts.py`:

   ```python
   NEW_CATEGORY_PROMPT = """Your optimized prompt here..."""
   ```

2. **Update Mapping**:

   ```python
   PROMPT_MAPPING = {
       # ... existing mappings
       "New Category": NEW_CATEGORY_PROMPT
   }
   ```

3. **Add Description** in `ui_components.py`:

   ```python
   category_descriptions = {
       # ... existing descriptions
       "New Category": "Description of new category"
   }
   ```

4. **Add Suggestions**:
   ```python
   suggestions = {
       # ... existing suggestions
       "New Category": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
   }
   ```

#### Adding a New AI Provider

1. **Extend `LLMProvider`** class:

   ```python
   def _init_new_provider(self):
       # Initialize new provider
       pass

   def _chat_new_provider(self, system_prompt, user_prompt, **kwargs):
       # Implement provider-specific chat method
       pass
   ```

2. **Update Provider Selection Logic**:
   ```python
   if self.new_provider_available:
       self.provider = "new_provider"
       self._init_new_provider()
   ```

---

## 🧪 Testing & Debugging

### Manual Testing Checklist

- [ ] **UI Components**: All buttons and inputs work correctly
- [ ] **Category Switching**: Sessions save properly when changing categories
- [ ] **AI Responses**: Both OpenAI and Ollama provide reasonable responses
- [ ] **Session Management**: Save, load, and delete operations work
- [ ] **Security Validation**: Blocked patterns are properly rejected
- [ ] **Error Handling**: Graceful failure for AI timeouts and errors

### Common Debugging Scenarios

#### Ollama Timeout Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check model availability
ollama list

# Restart Ollama if needed
ollama serve
```

#### OpenAI API Issues

```bash
# Verify API key in .env
cat .env | grep OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

#### Session Storage Issues

```bash
# Check session file
cat session_history.json

# Reset sessions if corrupted
rm session_history.json
```

### Performance Monitoring

Monitor these key metrics:

- **Response Time**: AI response generation time
- **Memory Usage**: Session state growth over time
- **Error Rate**: Frequency of AI failures
- **Session File Size**: Growth of session history

---

## 🚀 Extending the Application

### Potential Enhancements

#### 1. Advanced Analytics

- **Response Quality Scoring**: Analyze response quality over time
- **Progress Tracking**: Track improvement in different categories
- **Performance Metrics**: Response time, success rate, user engagement

#### 2. Enhanced AI Features

- **Multi-turn Conversations**: More complex interview simulations
- **Adaptive Difficulty**: Adjust question complexity based on performance
- **Voice Integration**: Speech-to-text and text-to-speech capabilities

#### 3. Collaboration Features

- **Session Sharing**: Share practice sessions with mentors
- **Group Practice**: Multi-user interview simulations
- **Expert Feedback**: Integration with human coaches

#### 4. Integration Capabilities

- **Calendar Integration**: Schedule practice sessions
- **Job Board APIs**: Analyze real job postings
- **CRM Integration**: Track application progress

### Architecture for Scaling

#### Database Migration

For production use, consider migrating from JSON files to a proper database:

```python
# Example: SQLite integration
import sqlite3

class DatabaseSessionManager(SessionManager):
    def __init__(self, db_path="sessions.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        # Create sessions table
        pass
```

#### API-First Design

Convert core functionality to REST APIs:

```python
# Example: FastAPI backend
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Process chat request
    pass
```

#### Microservices Architecture

Split into focused services:

- **Authentication Service**: User management
- **AI Service**: LLM provider management
- **Session Service**: Session persistence
- **Analytics Service**: Usage tracking and insights

---

## 🎯 Conclusion

The Interview Preparation Assistant demonstrates modern Python development practices with a clean, modular architecture. The strategic use of different AI prompting techniques, robust error handling, and thoughtful UX design make it both effective for users and maintainable for developers.

### Key Takeaways

1. **Modular Design**: Separation of concerns makes the codebase maintainable
2. **Strategic AI Usage**: Different prompting techniques optimize for different use cases
3. **Robust Error Handling**: Graceful failure and recovery enhance user experience
4. **Security First**: Multiple validation layers protect against misuse
5. **Extensible Architecture**: Easy to add new features and capabilities

### Contributing

To contribute to this project:

1. **Understand the Architecture**: Read this guide thoroughly
2. **Follow Code Standards**: Maintain the existing code quality
3. **Test Thoroughly**: Ensure your changes don't break existing functionality
4. **Document Changes**: Update this guide when adding new features

Welcome to the team! 🚀

---

_Created by Bernat Sampera for Turing College Sprint 1_
