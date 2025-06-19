# SuperZork: AI-Powered Text Adventure

A classic text adventure game enhanced with AI using Ollama and phi4-mini. Inspired by the legendary Zork series, SuperZork combines traditional text adventure gameplay with modern AI storytelling.

## Features

- **AI-Powered Storytelling**: Uses Ollama with phi4-mini for dynamic narrative generation
- **Dual Interface**: Play in terminal or retro-styled GUI
- **Dynamic Story Cards**: Configure your adventure with YAML story files
- **Character System**: Define players, companions, and NPCs with detailed character cards
- **Smart Context Management**: Intelligent token management for long adventures
- **Undo System**: Modify story outcomes on the fly
- **Debug Mode**: Peek behind the AI curtain

## Installation

1. Make sure you have Ollama installed and running with the phi4-mini model
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Terminal Mode
```bash
python superzork.py -s stories/zork_adventure.yaml
```

### GUI Mode  
```bash
python superzork_gui.py -s stories/zork_adventure.yaml
```

## Story Configuration

Stories are configured using YAML files. See `stories/zork_adventure.yaml` for an example.

## Controls

- Type your actions naturally
- `quit` - Exit the game
- `undo` - Modify the last AI response
- `debug` - Show conversation history
- `help` - Show available commands

## Credits

Inspired by the original Zork series and modern AI text adventure implementations.

This project was specifically inspired by [robjsliwa/ai_text_adventure](https://github.com/robjsliwa/ai_text_adventure), which demonstrates "Crafting Retro Text Adventure Games with Modern AI". SuperZork builds upon those concepts with enhanced features, improved error handling, external system prompts, and additional game modes.
