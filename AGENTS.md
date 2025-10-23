# AGENTS.md - Coding Guidelines for RecyFi

## Commands
- **Install dependencies**: `pip install -r server/requirements.txt`
- **Run server**: `cd server && python3 app.py`
- **Run full test**: `cd scripts && python3 test_flow.py`
- **Run single test**: `cd scripts && python3 -c "import test_flow; test_flow.main()"` (if test_flow.py had a main function)
- **Setup Orange Pi client**: `cd scripts && bash setup_client.sh`
- **Setup Orange Pi AP**: `cd scripts && bash setup_orange_pi.sh`
- **Run client manually**: `cd client && python3 orange_pi_client.py`

## Code Style
- **Language**: Python 3.x with Flask framework
- **Imports**: Standard library first, then third-party, grouped at top
- **Naming**: snake_case for variables/functions, PascalCase for classes (none present)
- **Formatting**: 4-space indentation, no trailing whitespace
- **Types**: No type hints used
- **Error handling**: Minimal, rely on Flask's built-in error handling
- **Logging**: Use print() for console feedback, file writes for persistence
- **Data storage**: JSON files for simple persistence
- **HTML**: Inline string templates in routes
- **Functions**: Keep short and focused, single responsibility
- **Constants**: UPPER_CASE for file paths and configuration values