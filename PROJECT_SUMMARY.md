# SuperZork: AI-Powered Text Adventure Game

## 🎮 Project Overview

SuperZork is a modern take on classic text adventure games, enhanced with AI capabilities using Ollama and the phi4-mini language model. It combines the nostalgic feel of games like Zork with dynamic, AI-generated storytelling that adapts to player actions in real-time.

## ✨ Key Features

### 🤖 AI-Powered Storytelling
- **Dynamic Narrative**: Stories adapt and evolve based on player choices
- **Natural Language Processing**: Type commands naturally, not just predefined verbs
- **Intelligent Responses**: AI handles unexpected actions creatively
- **Context Awareness**: The AI remembers previous actions and maintains story consistency

### 🎯 Dual Interface Options
- **Terminal Mode** (`superzork.py`): Classic command-line interface with colored output
- **GUI Mode** (`superzork_gui.py`): Retro-styled graphical interface with streaming text

### 📚 Story System
- **YAML Configuration**: Easy-to-edit story files with modular design
- **Character Cards**: Define players, companions, and NPCs with detailed backgrounds
- **Multiple Adventures**: Included stories cover different genres and themes
- **Extensible Design**: Create your own adventures by editing YAML files

### 🔧 Advanced Features
- **Smart Context Management**: Automatic token management for long adventures
- **Undo System**: Modify AI responses on the fly
- **Debug Mode**: Inspect conversation history and AI decision-making
- **Streaming Responses**: See AI generate text in real-time
- **Error Handling**: Graceful handling of network issues and AI errors

## 📁 Project Structure

```
SuperZork/
├── superzork.py              # Terminal version of the game
├── superzork_gui.py          # GUI version with retro styling
├── launcher.py               # Interactive game launcher
├── setup.py                  # Installation and setup script
├── validate_config.py        # Configuration file validator
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── setup.bat                 # Windows setup script
├── .gitignore               # Git ignore rules
├── .vscode/
│   └── tasks.json           # VS Code task definitions
└── stories/                 # Adventure story configurations
    ├── zork_adventure.yaml      # Classic underground empire adventure
    ├── blackwood_manor.yaml     # Gothic horror investigation
    ├── space_exploration.yaml   # Sci-fi first contact scenario
    └── detective_mystery.yaml   # Modern supernatural detective story
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+**: Make sure Python is installed and accessible
- **Ollama**: Install from https://ollama.ai/
- **phi4-mini Model**: The AI model used for story generation

### Quick Setup
1. **Run the setup script**:
   ```bash
   python setup.py
   ```
   This will:
   - Install Python dependencies
   - Check Ollama installation
   - Download phi4-mini model if needed
   - Validate the installation

2. **Alternative: Manual setup**:
   ```bash
   pip install -r requirements.txt
   ollama pull phi4-mini
   ```

### Running the Game

#### Interactive Launcher
```bash
python launcher.py
```
Choose your adventure and interface preference interactively.

#### Direct Execution
**Terminal Mode:**
```bash
python superzork.py -s stories/zork_adventure.yaml
```

**GUI Mode:**
```bash
python superzork_gui.py -s stories/zork_adventure.yaml
```

## 🎲 Available Adventures

### 1. **Zork Adventure** (`zork_adventure.yaml`)
- **Genre**: Classic Fantasy Adventure
- **Setting**: The Great Underground Empire
- **Companion**: Zyx the Sprite
- **Theme**: Exploration, puzzles, treasure hunting

### 2. **Blackwood Manor** (`blackwood_manor.yaml`)
- **Genre**: Gothic Horror
- **Setting**: Haunted Victorian mansion
- **Companion**: Dr. Elena Vasquez (Parapsychologist)
- **Theme**: Paranormal investigation, supernatural encounters

### 3. **Space Exploration** (`space_exploration.yaml`)
- **Genre**: Science Fiction
- **Setting**: Deep space, first contact scenario
- **Companions**: Commander Torres, ARIA (AI)
- **Theme**: Diplomacy, exploration, alien contact

### 4. **Detective Mystery** (`detective_mystery.yaml`)
- **Genre**: Supernatural Detective
- **Setting**: Modern Pacific Northwest
- **Companions**: Officer Rodriguez, Professor Blackwood
- **Theme**: Investigation, supernatural mystery, team-based solving

## 🎮 How to Play

### Basic Commands
- **Movement**: "go north", "enter building", "climb stairs"
- **Interaction**: "examine door", "take lamp", "use key"
- **Communication**: "talk to companion", "ask about history"
- **Inventory**: "check inventory", "drop item"
- **Observation**: "look around", "search room"

### Special Commands
- **quit**: Exit the game
- **undo**: Modify the last AI response
- **debug**: Show conversation history
- **help**: Display available commands

### AI Interaction Tips
- **Be Natural**: Type commands as you would speak them
- **Be Creative**: Try unusual approaches - the AI can handle them
- **Be Descriptive**: Detailed actions often get better responses
- **Be Patient**: The AI sometimes takes time to generate complex responses

## ⚙️ Configuration

### Story File Format (YAML)
```yaml
model: "phi4-mini"                    # AI model to use
ollama_url: "http://localhost:11434"  # Ollama server URL
num_tokens: 4096                      # Context window size
temperature: 0.7                      # AI creativity level (0.0-2.0)

player_card: |                       # Player character description
  Name: The Adventurer
  Description: ...

companion_cards:                     # Optional companion characters
  - |
    Name: Companion Name
    Description: ...

story_card: |                       # Main story setup and world description
  Setting: ...
  Mission: ...
  Background: ...
```

### Customization Options
- **Temperature**: Higher values (0.8-1.2) for more creative responses
- **Context Size**: Increase for longer adventures (up to model limits)
- **Story Elements**: Modify character backgrounds and world details
- **Companion Roles**: Add specialized knowledge or abilities

## 🛠️ Development Tools

### Configuration Validator
```bash
python validate_config.py                    # Validate all stories
python validate_config.py -f story.yaml     # Validate specific file
```

### VS Code Integration
- **Tasks**: Pre-configured build and run tasks
- **Launcher Integration**: Easy access to different game modes
- **Debugging Support**: Built-in terminal and debugging tools

### Batch Scripts (Windows)
```bash
setup.bat                             # Automated Windows setup
```

## 🔧 Technical Architecture

### AI Integration
- **Ollama API**: Local AI model serving
- **Streaming Responses**: Real-time text generation
- **Context Management**: Intelligent conversation pruning
- **Error Recovery**: Graceful handling of AI service issues

### User Interface
- **Terminal**: Colorized output using colorama
- **GUI**: Pygame-based retro terminal emulation
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Configuration System
- **YAML-Based**: Human-readable story definitions
- **Modular Design**: Separate player, companion, and story elements
- **Validation**: Built-in configuration checking

## 🌟 Advanced Features

### Story Modification System
- **Undo Mechanism**: Rewrite AI responses in real-time
- **Branching Narratives**: Create alternative story paths
- **Player Agency**: Direct control over story direction

### AI Prompt Engineering
- **System Prompts**: Carefully crafted for consistent behavior
- **Character Consistency**: Maintains personality across interactions
- **World Building**: Detailed setting and atmosphere guidance

### Performance Optimization
- **Token Management**: Automatic conversation pruning
- **Streaming Display**: Responsive text rendering
- **Resource Monitoring**: Efficient memory and processing usage

## 🎯 Use Cases

### Entertainment
- **Solo Gaming**: Immersive single-player adventures
- **Creative Writing**: AI-assisted story development
- **Nostalgia**: Modern take on classic text adventures

### Education
- **Creative Writing**: Learn storytelling techniques
- **AI Interaction**: Understand large language model capabilities
- **Programming**: Study Python game development patterns

### Development
- **AI Integration**: Example of practical LLM implementation
- **Game Engine**: Foundation for other text-based games
- **Configuration Systems**: YAML-based game content management

## 🚀 Future Enhancements

### Planned Features
- **Save/Load System**: Persistent game sessions
- **Multiplayer Support**: Collaborative adventures
- **Voice Interface**: Speech recognition and synthesis
- **Advanced AI Models**: Support for larger language models
- **Custom Model Training**: Fine-tuned adventure-specific models

### Community Features
- **Story Sharing**: Community-created adventures
- **Mod Support**: Plugin system for extensions
- **Online Repository**: Downloadable story packs

## 🤝 Contributing

SuperZork is designed to be extensible and community-friendly:

1. **Create New Stories**: Write YAML configuration files
2. **Improve AI Prompts**: Enhance the storytelling quality
3. **Add Features**: Extend functionality in Python
4. **Test and Debug**: Help identify and fix issues
5. **Documentation**: Improve guides and examples

## 📜 Credits and Inspiration

- **Zork Series**: The legendary text adventure games by Infocom
- **AI Text Adventure**: Inspired by robjsliwa/ai_text_adventure
- **Inform**: The interactive fiction programming language
- **Modern AI**: Leveraging Ollama and open-source language models

## 🎉 Conclusion

SuperZork represents the fusion of classic text adventure gaming with modern AI capabilities. It offers both the nostalgic experience of traditional interactive fiction and the dynamic storytelling possibilities of large language models. Whether you're a fan of classic adventures, interested in AI applications, or looking for a creative writing tool, SuperZork provides an engaging platform for exploration and creativity.

The modular design makes it easy to create new adventures, while the AI integration ensures that every playthrough offers unique experiences. With both terminal and GUI interfaces, comprehensive configuration options, and robust development tools, SuperZork is designed to be accessible to players and developers alike.

Ready to explore the Great Underground Empire? The adventure awaits!
