
# SuperZork Copilot Instructions

These guidelines are for AI coding agents working on the SuperZork codebase. Follow these project-specific rules and conventions to maximize productivity and maintain code quality.

## 1. Git & Workflow
- **Branching:** For any GitHub issue, create a new branch: `issue-<number>-<short-description>` (e.g., `issue-42-fix-ui-layout`).
- **Commits:** Only commit when the code is stable and reviewed. Use [Gitmoji](https://gitmoji.dev/) in commit messages and PR titles (e.g., `✨ Add GUI retro terminal mode`).
- **Agent Mode:** Before completing a task, check for errors, warnings, or inconsistencies. Address all outstanding issues before finalizing.
- **Commit Messages:** Be descriptive and meaningful. Summarize the change clearly.

## 2. Project Architecture & Key Files
- **Main Game Logic:**
  - `superzork.py`: Terminal version (core game loop, AI integration, command parsing)
  - `superzork_gui.py`: GUI version (Pygame-based retro terminal)
  - `launcher.py`: Interactive launcher for selecting stories and interface
- **Story System:**
  - `stories/*.yaml`: Modular YAML files define adventures (player, companions, world, settings)
  - `prompts/system_prompt.txt`: System prompt for AI Dungeon Master behavior
- **Validation & Testing:**
  - `validate_config.py`: Validates YAML story files (run after editing/adding stories)
  - `test_superzork.py`: Runs import, config, and system tests
- **Setup:**
  - `setup.py` and `setup.bat`: Install dependencies, check Ollama, download models
  - `requirements.txt`: Python dependencies (colorama, PyYAML, requests, pygame)

## 3. Developer Workflows
- **Setup:**
  - Run `python setup.py` (cross-platform) or `setup.bat` (Windows) to install dependencies and check Ollama/phi4-mini model.
- **Testing:**
  - Run `python test_superzork.py` for a full test suite.
  - Run `python validate_config.py` to validate all story YAMLs.
- **Running the Game:**
  - Terminal: `python superzork.py -s stories/zork_adventure.yaml`
  - GUI: `python superzork_gui.py -s stories/zork_adventure.yaml`
  - Launcher: `python launcher.py` (interactive mode)
- **Story Editing:**
  - Copy an existing YAML in `stories/`, edit `story_card` and `player_card`, then validate.
- **System Prompt:**
  - Edit `prompts/system_prompt.txt` to change AI behavior for all stories.

## 4. Project Conventions & Patterns
- **YAML Story Files:**
  - Required fields: `model`, `story_card`, `player_card`
  - Optional: `ollama_url`, `num_tokens`, `temperature`, `companion_cards`
  - Use multi-line strings for cards; keep descriptions vivid and concise.
- **AI Integration:**
  - Uses Ollama API (default: `http://localhost:11434`) and `phi4-mini` model.
  - All AI prompts and responses are streamed for real-time feedback.
- **Undo/Debug:**
  - Both terminal and GUI support `undo` (modify last AI response) and `debug` (show conversation history).
- **Error Handling:**
  - All user-facing scripts handle missing files, YAML errors, and AI connection issues gracefully.
- **Extensibility:**
  - New stories: Add YAML to `stories/` and validate.
  - New features: Extend `superzork.py`/`superzork_gui.py` with clear separation of UI and game logic.

## 5. Integration & External Dependencies
- **Ollama:**
  - Must be installed and running locally. Use `ollama pull phi4-mini` to ensure the model is available.
- **Python 3.8+** is required.
- **Pygame** is required for GUI mode.

## 6. Examples & Best Practices
- **Add a new adventure:**
  1. Copy `stories/zork_adventure.yaml` to `stories/my_adventure.yaml`
  2. Edit `story_card`, `player_card`, and companions as needed
  3. Run `python validate_config.py -f stories/my_adventure.yaml`
- **Update system prompt:**
  - Edit `prompts/system_prompt.txt` and restart the game for changes to take effect.
- **Run all tests before PR:**
  - `python test_superzork.py` and `python validate_config.py`

## 7. References
- See `README.md` and `PROJECT_SUMMARY.md` for more details on architecture, features, and usage.
- For troubleshooting, check error messages in the terminal or GUI; most issues are reported with actionable feedback.

---
**If any section is unclear or incomplete, please provide feedback for further refinement.**