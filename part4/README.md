# 🎯 Interview Preparation Assistant

A comprehensive, modular Streamlit-based web application for practicing interview skills with AI assistance. The app supports both OpenAI and Ollama backends with automatic fallback functionality and robust timeout handling.

## ✨ Features

- **Multiple Interview Categories**: Practice across 5 different interview types
- **Dual AI Backend Support**: Automatic detection and fallback between OpenAI and Ollama
- **Advanced System Prompts**: 5 different prompting techniques implemented
- **Security Measures**: Input validation, sanitization, and prompt injection protection
- **Session Management**: Save and reload previous practice sessions with export functionality
- **Tunable Parameters**: Adjust AI creativity with temperature controls
- **Modular Architecture**: Clean, maintainable code structure with separated concerns
- **Robust Error Handling**: Timeout management, retry logic, and graceful failure handling
- **Clean UI**: Modern, responsive Streamlit interface

## 🏗️ Project Structure

```
interview-prep/
├── app.py                 # Main application controller (refactored & clean)
├── llm_provider.py        # Unified LLM provider with timeout handling
├── session_manager.py     # Session persistence and history management
├── ui_components.py       # Reusable Streamlit UI components
├── chat_handler.py        # Chat interaction and message processing
├── system_prompts.py      # System prompts with different techniques
├── security.py           # Input validation and security measures
├── pyproject.toml         # uv dependency management
├── .env                   # Environment configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Optional: [Ollama](https://ollama.ai) for local AI (if not using OpenAI)

### Installation

1. **Clone or navigate to the project directory**:

   ```bash
   cd part4
   ```

2. **Install dependencies using uv**:

   ```bash
   uv sync
   ```

3. **Configure environment variables**:
   Edit the `.env` file and optionally add your OpenAI API key:

   ```bash
   # Uncomment and add your key for OpenAI
   OPENAI_API_KEY=your_openai_api_key_here

   # Ollama settings (used as fallback)
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=gemma2:4b
   ```

4. **For Ollama users** (if not using OpenAI):

   ```bash
   # Install and start Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull gemma2:4b
   ollama serve
   ```

5. **Run the application**:

   ```bash
   uv run streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 🔧 New Architecture Benefits

### Modular Design

- **Separation of Concerns**: Each module handles specific functionality
- **Maintainability**: Easy to update individual components
- **Testability**: Components can be tested independently
- **Extensibility**: Simple to add new features

### Key Modules

#### `app.py` - Main Controller

- Orchestrates all components
- Handles application flow
- Much cleaner and focused

#### `session_manager.py` - Session Management

- Session persistence and loading
- History management with export capabilities
- Session cleanup and organization

#### `ui_components.py` - UI Components

- Reusable Streamlit components
- Consistent UI patterns
- Simplified interface management

#### `chat_handler.py` - Chat Logic

- Message processing and validation
- AI response coordination
- Chat state management

#### `llm_provider.py` - Enhanced AI Backend

- **Improved Timeout Handling**: Configurable timeouts for different operations
- **Retry Logic**: Exponential backoff for failed requests
- **Better Error Messages**: More informative error reporting
- **Resource Management**: Proper connection cleanup

## 📚 Interview Categories & Prompting Techniques

### 1. Behavioral Questions (Few-shot Learning)

- Uses examples to demonstrate proper STAR method responses
- Provides feedback based on demonstrated patterns
- **Example prompts**: Teamwork scenarios, conflict resolution

### 2. Technical Questions (Zero-shot)

- Direct technical assessment without examples
- Focuses on problem-solving and communication
- **Example prompts**: Python coding, system design basics

### 3. Job Description Analysis (Chain-of-thought)

- Step-by-step methodical analysis approach
- Breaks down requirements systematically
- **Example prompts**: Role requirement analysis, preparation strategies

### 4. Final Interview Strategies (Role Prompting)

- AI takes on CEO/executive interviewer persona
- Focuses on cultural fit and strategic thinking
- **Example prompts**: Company culture questions, leadership scenarios

### 5. System Design (Instruction-based)

- Detailed instructions for conducting system design interviews
- Structured evaluation criteria
- **Example prompts**: Architecture design, scalability discussions

## 🛡️ Enhanced Security & Reliability

### Ollama Timeout Fixes

- **Connection Timeout**: 10 seconds for initial connection
- **Read Timeout**: 120 seconds for AI response generation
- **Retry Logic**: Up to 3 attempts with exponential backoff
- **Better Error Messages**: Clear guidance on timeout issues

### Security Features

- **Input Length Limits**: 5000 characters maximum
- **Pattern Blocking**: Prevents prompt injection attempts
- **Content Filtering**: Blocks sensitive terms and system prompts
- **Input Sanitization**: Removes harmful content automatically
- **Response Validation**: Quality checks on AI responses

### Error Handling

- **Graceful Degradation**: App continues working even with AI issues
- **Clear Error Messages**: User-friendly error reporting
- **Automatic Recovery**: Retry mechanisms for transient failures

## 💾 Enhanced Session Management

- **Auto-save**: Sessions saved when switching categories
- **Manual Save**: Save button with success feedback
- **Session History**: View, load, and delete past sessions
- **Session Export**: Export sessions in JSON or text format
- **Local Storage**: JSON file-based session persistence
- **Session Previews**: Quick preview of session content

## 🎯 Usage Tips

1. **Start with Suggestions**: Use quick-start buttons for common scenarios
2. **Adjust Temperature**: Lower for focused responses, higher for creativity
3. **Save Important Sessions**: Use the save feature for valuable conversations
4. **Switch Categories**: Practice different interview types in one session
5. **Review History**: Learn from past practice sessions with export feature
6. **Handle Timeouts**: If using Ollama, be patient with longer responses

## 🔍 Troubleshooting

### Common Issues

1. **Ollama Timeout Errors**

   - **Fixed in v2.0**: Enhanced timeout handling and retry logic
   - Ensure Ollama is running: `ollama serve`
   - Check model is installed: `ollama list`
   - Verify correct model name in `.env`
   - Try shorter prompts if still experiencing issues

2. **OpenAI API Errors**

   - Verify API key is correct in `.env`
   - Check API quota and billing
   - Ensure internet connectivity

3. **Import Errors**

   - Run `uv sync` to install dependencies
   - Check Python version (3.12+ required)

4. **Module Import Issues**
   - All modules are now properly structured
   - Use `uv run streamlit run app.py` to ensure proper environment

### Performance Tips

- Use OpenAI for faster responses
- Lower temperature for more consistent results
- Clear chat history for better performance
- Save important sessions before long conversations
- Export sessions for external review and analysis

## 🆕 What's New in v2.0

### Fixed Issues

- ✅ **Ollama Timeout Issues**: Robust timeout handling and retry logic
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Better Error Handling**: Graceful failure and recovery
- ✅ **Enhanced Session Management**: Export and better organization

### New Features

- 🎉 **Response Validation**: Quality checks on AI responses
- 🎉 **Response Enhancement**: Category-specific tips and suggestions
- 🎉 **Session Export**: Export conversations in multiple formats
- 🎉 **Better UI Feedback**: Clear success/error messaging
- 🎉 **Improved Architecture**: Maintainable and extensible codebase

## 🤝 Contributing

This project uses:

- **uv** for dependency management
- **Streamlit** for the web interface
- **OpenAI** and **Ollama** for AI capabilities
- **Python 3.12+** as the runtime
- **Modular Design** for maintainability

## 📝 License

This project is provided as-is for educational and practice purposes.

## 🎉 Getting Started

Ready to improve your interview skills with the enhanced, modular app?

```bash
uv run streamlit run app.py
```

**New users**: Try the quick suggestions to get started quickly!  
**Returning users**: Check out the improved session management and export features!

Happy interviewing! 🚀
