"""
LLM Provider module for Interview Preparation App.
Supports both OpenAI and Ollama backends with automatic fallback.
"""

import os
import httpx
import time
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider:
    """
    A unified LLM provider that automatically detects available backends
    and provides a consistent chat interface.
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma2:4b")
        
        # Initialize the appropriate client
        if self.openai_api_key and self.openai_api_key.strip():
            self.provider = "openai"
            self._init_openai()
        else:
            self.provider = "ollama"
            self._init_ollama()
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model = "gpt-3.5-turbo"  # Default model
        except ImportError:
            raise ImportError("OpenAI package not found. Please install it with: uv add openai")
    
    def _init_ollama(self):
        """Initialize Ollama client with proper timeout settings."""
        # Configure timeouts: 10s connect, 120s read, 180s total
        timeout = httpx.Timeout(
            connect=10.0,  # Connection timeout
            read=120.0,    # Read timeout for long responses
            write=30.0,    # Write timeout
            pool=180.0     # Pool timeout
        )
        
        self.client = httpx.Client(
            base_url=self.ollama_base_url,
            timeout=timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        self.model = self.ollama_model
    
    def _is_ollama_available(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            # Quick health check with shorter timeout
            response = self.client.get("/api/tags", timeout=5.0)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model.get("name", "").startswith(self.ollama_model) for model in models)
            return False
        except (httpx.TimeoutException, httpx.ConnectError, Exception):
            return False
    
    def chat(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """
        Unified chat method that works with both OpenAI and Ollama.
        
        Args:
            system_prompt: The system prompt to set context
            user_prompt: The user's input prompt
            **kwargs: Additional parameters like temperature, max_tokens, etc.
        
        Returns:
            str: The AI response
        """
        if self.provider == "openai":
            return self._chat_openai(system_prompt, user_prompt, **kwargs)
        else:
            return self._chat_ollama(system_prompt, user_prompt, **kwargs)
    
    def _chat_openai(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Chat using OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Extract OpenAI-specific parameters
            temperature = kwargs.get("temperature", 0.7)
            max_tokens = kwargs.get("max_tokens", 1000)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"
    
    def _chat_ollama(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Chat using Ollama API with retry logic."""
        max_retries = 2
        base_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # Check if Ollama is available
                if not self._is_ollama_available():
                    return f"Ollama is not running or model '{self.ollama_model}' is not available. Please start Ollama and ensure the model is installed."
                
                temperature = kwargs.get("temperature", 0.7)
                
                # Combine system and user prompts for Ollama
                combined_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
                
                payload = {
                    "model": self.model,
                    "prompt": combined_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": 1000,  # Limit response length
                        "stop": ["User:", "System:"]  # Stop tokens
                    }
                }
                
                # Make request with explicit timeout
                response = self.client.post(
                    "/api/generate", 
                    json=payload,
                    timeout=120.0  # 2 minutes for generation
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "No response received").strip()
                else:
                    error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                    if attempt < max_retries:
                        time.sleep(base_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    return error_msg
                    
            except httpx.TimeoutException:
                if attempt < max_retries:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return f"Ollama request timed out after {attempt + 1} attempts. The model might be processing a complex request or the system is overloaded. Try again with a shorter prompt or restart Ollama."
            
            except httpx.ConnectError:
                return f"Cannot connect to Ollama at {self.ollama_base_url}. Please ensure Ollama is running with: ollama serve"
            
            except Exception as e:
                if attempt < max_retries:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                return f"Error with Ollama: {str(e)}"
        
        return "Failed to get response after multiple attempts."
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider."""
        return {
            "provider": self.provider,
            "model": self.model,
            "available": True if self.provider == "openai" else self._is_ollama_available()
        }
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'client') and isinstance(self.client, httpx.Client):
            self.client.close() 