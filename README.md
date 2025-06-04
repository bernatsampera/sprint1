# Sprint 1 Part 3: Introduction to Prompt Engineering

This notebook introduces the basics of prompt engineering using OpenAI and Google's Gemini models.

## Setup for Cursor IDE

### Prerequisites

- `uv` package manager installed
- API keys for OpenAI and Google Gemini

### Quick Start

1. **Activate the virtual environment** (if not already active):

   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies** (already done):

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up your API keys**:

   - Edit the `.env` file that was created
   - Replace the placeholder values with your actual API keys:
     ```
     OPENAI_API_KEY=your_actual_openai_api_key_here
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
     ```

4. **Open the notebook in Cursor**:

   - Open `Sprint1_part3_intro_to_prompt_engineering.ipynb`
   - When prompted, select the kernel: **"Sprint 1 - Prompt Engineering"**
   - If the kernel doesn't appear, restart Cursor and try again

5. **Run the notebook**:
   - Run cells in order
   - The first cell will verify your API keys are set up correctly

## Troubleshooting

### Kernel Issues

If you can't see the "Sprint 1 - Prompt Engineering" kernel in Cursor:

1. Make sure you're in the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Reinstall the kernel:

   ```bash
   python -m ipykernel install --user --name=sprint1-prompt-engineering --display-name="Sprint 1 - Prompt Engineering"
   ```

3. Restart Cursor IDE

### Dependency Issues

If you encounter package conflicts:

1. Check your virtual environment is active:

   ```bash
   which python  # Should show path to .venv/bin/python
   ```

2. Run the setup script to verify everything is installed:
   ```bash
   python setup_notebook.py
   ```

### API Key Issues

- Make sure your `.env` file exists and contains valid API keys
- The notebook will show ✅ or ❌ indicators for each API key when you run the setup cell

## What's Included

- **Virtual Environment**: Isolated Python environment with all dependencies
- **Requirements File**: Exact package versions to avoid conflicts
- **Jupyter Kernel**: Dedicated kernel for this project
- **Environment Setup**: Secure API key management
- **Setup Script**: Automated verification and setup

## Running Without Jupyter

You can also run individual Python scripts using the virtual environment:

```bash
# Make sure virtual environment is active
source .venv/bin/activate

# Run any Python script
python your_script.py
```

## Dependencies

The project includes these main packages:

- `openai` - OpenAI API client
- `google-generativeai` - Google Gemini API client
- `tiktoken` - OpenAI's tokenizer
- `jupyter` - Jupyter notebook environment
- `python-dotenv` - Environment variable management

All dependency conflicts have been resolved in the `requirements.txt` file.
