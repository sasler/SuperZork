# SuperZork: AI-Powered Text Adventure

A classic text adventure game enhanced with AI using multiple backends. Inspired by the legendary Zork series, SuperZork combines traditional text adventure gameplay with modern AI storytelling.

## 🎮 Features

- **Multiple AI Backends**: 
  - **Ollama** (local AI models like phi4-mini)
  - **Hugging Face MCP** (cloud-based models)
- **Dual Interface**: Play in terminal or retro-styled GUI
- **Dynamic Story Cards**: Configure your adventure with YAML story files
- **Character System**: Define players, companions, and NPCs with detailed character cards
- **External System Prompt**: Easily customizable AI behavior via external prompt file
- **Smart Context Management**: Intelligent token management for long adventures
- **Enhanced Error Handling**: Robust timeout management and connection recovery
- **Undo System**: Modify story outcomes on the fly
- **Debug Mode**: Peek behind the AI curtain
- **Multiple Story Templates**: Classic Zork, horror, sci-fi, detective, and cloud-AI themes
- **Validation Tools**: Built-in configuration validation and testing

## 🚀 Installation

### Prerequisites
- Python 3.8+
- **Either**:
  - [Ollama](https://ollama.ai/) installed and running with phi4-mini model: `ollama pull phi4-mini`
  - **Or** Hugging Face MCP: `pip install mcp`

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
# Using Ollama (default)
python superzork.py -s stories/zork_adventure.yaml

# Using Hugging Face MCP
python superzork.py -s stories/huggingface_adventure.yaml --backend huggingface

# Override backend in configuration
python superzork.py -s stories/zork_adventure.yaml -b huggingface
```

### GUI Mode  
```bash
# Using Ollama (default)
python superzork_gui.py -s stories/zork_adventure.yaml

# Using Hugging Face MCP
python superzork_gui.py -s stories/huggingface_adventure.yaml --backend huggingface
```

### Available Stories
- **zork_adventure.yaml** - Classic underground empire exploration (Ollama)
- **huggingface_adventure.yaml** - Cloud-AI powered exploration (Hugging Face MCP)
- **blackwood_manor.yaml** - Gothic horror mystery
- **space_exploration.yaml** - Sci-fi alien planet adventure
- **detective_mystery.yaml** - Noir crime investigation

## ⚙️ Configuration

### Story Configuration
Stories are configured using YAML files. Example structure:

```yaml
# AI Backend Configuration
ai_backend: "ollama"  # Options: "ollama", "huggingface"
model: "phi4-mini"

# Ollama-specific settings
ollama_url: "http://localhost:11434"

# Hugging Face-specific settings  
hf_model: "microsoft/DialoGPT-large"
hf_token: null  # Optional: for private models
max_tokens: 1024

# Common settings
num_tokens: 4096
temperature: 0.7

story_card: |
  You find yourself in the Great Underground Empire...

player_card: |
  You are a brave adventurer...

companion_cards:
  - "A wise old wizard who speaks in riddles"
```

### AI Backend Options

#### Ollama Backend
- **Pros**: Fast local inference, privacy, no API costs
- **Cons**: Requires local installation and model downloads
- **Setup**: Install Ollama and run `ollama pull phi4-mini`

#### Hugging Face Backend  
- **Pros**: Access to diverse cloud models, no local setup required
- **Cons**: Requires internet connection, may need API token for best experience
- **Setup**: 
  1. For basic access: Works without setup (rate-limited)
  2. For full access: Get a free API token from [Hugging Face](https://huggingface.co/settings/tokens)
  3. Add `hf_token: "your_token_here"` to your story YAML configuration

### Getting a Hugging Face API Token
1. Create a free account at [huggingface.co](https://huggingface.co/)
2. Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Click "New token" and create a token with "Read" permissions
4. Copy the token and add it to your story configuration:
   ```yaml
   hf_token: "hf_your_token_here"
   ```

### System Prompt Customization
Edit `prompts/system_prompt.txt` to customize the AI's behavior and personality.

## 🎮 Controls

- Type your actions naturally: "go north", "examine door", "take lamp"
- **quit** - Exit the game
- **undo** - Modify the last AI response
- **debug** - Show conversation history
- **help** - Show available commands and current backend info

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
2. Modify the `ai_backend`, `story_card`, and `player_card` sections
3. Configure backend-specific settings (Ollama URL, HF models, etc.)
4. Validate: `python validate_config.py your_story.yaml`

## 📁 Project Structure

```
SuperZork/
├── superzork.py              # Main terminal game
├── superzork_gui.py          # GUI version
├── ai_clients.py             # AI backend implementations
├── launcher.py               # Interactive launcher
├── test_superzork.py         # Test suite
├── validate_config.py        # Configuration validator
├── requirements.txt          # Dependencies
├── prompts/
│   └── system_prompt.txt    # External AI system prompt
├── stories/                  # Story configurations
│   ├── zork_adventure.yaml
│   ├── huggingface_adventure.yaml
│   ├── blackwood_manor.yaml
│   ├── space_exploration.yaml
│   └── detective_mystery.yaml
└── .vscode/tasks.json        # VS Code tasks
```

## Credits

Inspired by the original Zork series and modern AI text adventure implementations.

This project was specifically inspired by [robjsliwa/ai_text_adventure](https://github.com/robjsliwa/ai_text_adventure), which demonstrates "Crafting Retro Text Adventure Games with Modern AI". SuperZork builds upon those concepts with enhanced features, improved error handling, external system prompts, and additional game modes.
