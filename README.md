# Sprint 1 Part 3: Introduction to Prompt Engineering

## Setup (3 steps)

1. **Create virtual environment with pip**:

   ```bash
   uv venv .venv --seed
   source .venv/bin/activate
   uv pip install jupyter ipykernel
   python -m ipykernel install --user --name=sprint1-prompt-engineering --display-name 'Sprint 1 - Prompt Engineering'
   ```

2. **Add your API keys** to the notebook (edit the cell with OPENAI_API_KEY, etc.)

3. **Open and run the notebook** - select "Sprint 1 - Prompt Engineering" kernel

That's it. All packages will install automatically via `%pip install` in the notebook cells.
