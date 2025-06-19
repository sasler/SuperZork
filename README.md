# SuperZork: AI-Powered Text Adventure

A classic text adventure game enhanced with AI using Ollama and phi4-mini. Inspired by the legendary Zork series, SuperZork combines traditional text adventure gameplay with modern AI storytelling.

## 🎮 Features

- **AI-Powered Storytelling**: Uses Ollama with phi4-mini for dynamic narrative generation
- **Dual Interface**: Play in terminal or retro-styled GUI
- **Dynamic Story Cards**: Configure your adventure with YAML story files
- **Character System**: Define players, companions, and NPCs with detailed character cards
- **External System Prompt**: Easily customizable AI behavior via external prompt file
- **Smart Context Management**: Intelligent token management for long adventures
- **Enhanced Error Handling**: Robust timeout management and connection recovery
- **Undo System**: Modify story outcomes on the fly
- **Debug Mode**: Peek behind the AI curtain
- **Multiple Story Templates**: Classic Zork, horror, sci-fi, and detective themes
- **Validation Tools**: Built-in configuration validation and testing

## 🚀 Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- phi4-mini model: `ollama pull phi4-mini`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/sasler/SuperZork.git
   cd SuperZork
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python test_superzork.py
   ```

## 🎯 Usage

### Quick Start
```bash
# Interactive launcher
python launcher.py
```

### Terminal Mode
```bash
python superzork.py -s stories/zork_adventure.yaml
```

### GUI Mode  
```bash
python superzork_gui.py -s stories/zork_adventure.yaml
```

### Available Stories
- **zork_adventure.yaml** - Classic underground empire exploration
- **blackwood_manor.yaml** - Gothic horror mystery
- **space_exploration.yaml** - Sci-fi alien planet adventure
- **detective_mystery.yaml** - Noir crime investigation

## ⚙️ Configuration

### Story Configuration
Stories are configured using YAML files. Example structure:

```yaml
model: "phi4-mini"
ollama_url: "http://localhost:11434"
num_tokens: 4096
temperature: 0.7

story_card: |
  You find yourself in the Great Underground Empire...

player_card: |
  You are a brave adventurer...

companion_cards:
  - "A wise old wizard who speaks in riddles"
```

### System Prompt Customization
Edit `prompts/system_prompt.txt` to customize the AI's behavior and personality.

## 🎮 Controls

- Type your actions naturally: "go north", "examine door", "take lamp"
- **quit** - Exit the game
- **undo** - Modify the last AI response
- **debug** - Show conversation history
- **help** - Show available commands

## 🛠️ Development

### Testing
```bash
# Run full test suite
python test_superzork.py

# Validate story configurations
python validate_config.py
```

### Creating New Stories
1. Copy an existing story YAML file
2. Modify the `story_card` and `player_card` sections
3. Validate: `python validate_config.py your_story.yaml`

## 📁 Project Structure

```
SuperZork/
├── superzork.py              # Main terminal game
├── superzork_gui.py          # GUI version
├── launcher.py               # Interactive launcher
├── test_superzork.py         # Test suite
├── validate_config.py        # Configuration validator
├── requirements.txt          # Dependencies
├── prompts/
│   └── system_prompt.txt    # External AI system prompt
├── stories/                  # Story configurations
│   ├── zork_adventure.yaml
│   ├── blackwood_manor.yaml
│   ├── space_exploration.yaml
│   └── detective_mystery.yaml
└── .vscode/tasks.json        # VS Code tasks
```

## Credits

Inspired by the original Zork series and modern AI text adventure implementations.

This project was specifically inspired by [robjsliwa/ai_text_adventure](https://github.com/robjsliwa/ai_text_adventure), which demonstrates "Crafting Retro Text Adventure Games with Modern AI". SuperZork builds upon those concepts with enhanced features, improved error handling, external system prompts, and additional game modes.
