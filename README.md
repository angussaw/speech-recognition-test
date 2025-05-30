# <Project Name>

## A. Developer Setup

### Installation

1. Install UV:

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies using UV:

   ```
   uv sync
   ```

4. Install pre-commit hooks:

   ```
   pre-commit install
   ```
