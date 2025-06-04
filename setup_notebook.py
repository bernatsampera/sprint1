#!/usr/bin/env python3
"""
Setup script for Sprint 1 Part 3: Introduction to Prompt Engineering
This script helps configure the environment for running the notebook in Cursor IDE.
"""

import os
import sys
from pathlib import Path

def check_virtual_env():
    """Check if we're in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'openai',
        'google.generativeai',
        'tiktoken',
        'jupyter',
        'ipykernel'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    return missing_packages

def create_env_file():
    """Create a .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# API Keys for Prompt Engineering
# Replace the placeholder values with your actual API keys

OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Set default model names
OPENAI_MODEL=gpt-3.5-turbo
GEMINI_MODEL=gemini-pro
"""
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ Created .env file template")
            print("📝 Please edit the .env file and add your actual API keys")
        except Exception as e:
            print(f"❌ Could not create .env file: {e}")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up Sprint 1 Part 3: Prompt Engineering Environment")
    print("=" * 60)
    
    # Check virtual environment
    if check_virtual_env():
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not in a virtual environment. Consider activating one.")
    
    print("\n📦 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("💡 Run: uv pip install -r requirements.txt")
        return 1
    else:
        print("\n✅ All required packages are installed!")
    
    print("\n🔑 Setting up environment file...")
    create_env_file()
    
    print("\n🎯 Next Steps:")
    print("1. Edit the .env file and add your API keys")
    print("2. In Cursor, open the notebook: Sprint1_part3_intro_to_prompt_engineering.ipynb")
    print("3. Select the kernel: 'Sprint 1 - Prompt Engineering'")
    print("4. Run the cells in order")
    
    print("\n✨ Setup complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 