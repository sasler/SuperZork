#!/usr/bin/env python3
"""
SuperZork: AI-Powered Text Adventure Game
GUI Version with Retro Styling

A classic text adventure game enhanced with AI using multiple backends:
- Ollama (local AI models)
- Hugging Face MCP (cloud-based models)

Features a retro-styled graphical interface reminiscent of classic computer terminals.
"""

import pygame
import sys
import yaml
import argparse
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from colorama import Fore, init

# Import our AI client system
from ai_clients import create_ai_client, get_available_backends, Message

# Initialize colorama for console output
init(autoreset=True)

# Initialize pygame
pygame.init()


class GameConfig:
    """Configuration class for the GUI game"""
    
    def __init__(self, story_path: str, backend: str = None):
        """Initialize configuration with default values"""
        # Display settings
        self.width, self.height = 1200, 800
        self.font_size = 18
        
        # Try to use a monospace font, fall back to default if not available
        self.font = self._load_font()
        self.line_height = self.font.get_height() + 4
        
        # Color scheme - retro terminal colors
        self.colors = {
            'black': (0, 0, 0),
            'dark_green': (0, 120, 0),
            'green': (0, 255, 0),
            'amber': (255, 191, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'blue': (0, 150, 255),
            'cyan': (0, 255, 255),
            'gray': (128, 128, 128),
            'dark_gray': (64, 64, 64)
        }
        
        # Store backend override
        self.backend_override = backend
        
        # Load story configuration
        self.load_config(story_path)
    
    def _load_font(self) -> pygame.font.Font:
        """Load the best available monospace font"""
        # Try common monospace fonts
        font_names = [
            'Consolas',
            'Courier New', 
            'Liberation Mono',
            'DejaVu Sans Mono',
            'monospace'
        ]
        
        for font_name in font_names:
            try:
                font = pygame.font.SysFont(font_name, self.font_size)
                if font:
                    return font
            except:
                continue
        
        # Fall back to default font
        return pygame.font.Font(None, self.font_size)
    
    def load_config(self, path: str) -> None:
        """Load configuration from YAML file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Determine AI backend
            self.ai_backend = self.backend_override or config.get('ai_backend', 'ollama')
            
            # Common settings
            self.num_ctx = config.get('num_tokens', 4096)
            self.temperature = config.get('temperature', 0.7)
            
            # Backend-specific model selection
            if self.ai_backend.lower() == 'ollama':
                self.model = config.get('model', 'phi4-mini')
                ai_config = {
                    'ollama_url': config.get('ollama_url', 'http://localhost:11434'),
                    'num_tokens': self.num_ctx,
                    'temperature': self.temperature
                }
            elif self.ai_backend.lower() == 'huggingface':
                self.model = config.get('hf_model', config.get('model', 'microsoft/DialoGPT-large'))
                ai_config = {
                    'hf_token': config.get('hf_token'),
                    'max_tokens': config.get('max_tokens', 1024),
                    'temperature': self.temperature
                }
            else:
                raise ValueError(f"Unknown AI backend: {self.ai_backend}")
            
            # Create AI client
            try:
                self.ai_client = create_ai_client(self.ai_backend, self.model, **ai_config)
                if not self.ai_client.is_available():
                    raise ConnectionError(f"{self.ai_backend} backend is not available")
            except Exception as e:
                print(f"{Fore.RED}Error initializing {self.ai_backend} backend: {e}")
                available = get_available_backends()
                if available:
                    print(f"{Fore.YELLOW}Available backends: {', '.join(available)}")
                else:
                    print(f"{Fore.RED}No AI backends are currently available!")
                sys.exit(1)
            
            # Story elements
            self.player_card = config.get('player_card', '')
            self.companion_cards = config.get('companion_cards', [])
            self.story_card = config.get('story_card', '')
            
            if not self.story_card:
                raise ValueError("Story card is required but not found in configuration")
                
        except FileNotFoundError:
            print(f"{Fore.RED}Story file not found: {path}")
            sys.exit(1)
        except yaml.YAMLError as exc:
            print(f"{Fore.RED}Error parsing YAML file: {exc}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}Configuration error: {e}")
            sys.exit(1)


class SuperZorkGUI:
    """Main GUI game class"""
    
    def __init__(self, config: GameConfig):
        """Initialize the GUI game"""
        self.config = config
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption("SuperZork: The Great Underground Empire Awakens")
        
        # Game state
        self.messages = []
        self.display_messages = []
        self.is_story_update = False
        self.scroll_offset = 0
        
        # Text input
        self.input_text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # AI streaming
        self.text_generator = None
        self.next_word_time = 0
        self.is_ai_typing = False
        
        # UI constants
        self.input_height = 40
        self.margin = 20
        self.text_area_height = self.config.height - self.input_height - self.margin * 2
        
    def build_story_system_prompt(self) -> tuple[str, str]:
        """Build the initial system prompt and first message"""
        story_system_prompt = self.load_system_prompt()

        companions_str = '\n'.join(self.config.companion_cards)
        start_message = f"""Initialize the SuperZork adventure using the following information:

STORY SETTING:
```
{self.config.story_card}
```

PLAYER CHARACTER:
```
{self.config.player_card}
```

COMPANION CHARACTERS:
```
{companions_str}
```

Begin the adventure with an atmospheric description of the player's current situation and surroundings. Set the scene for the underground empire exploration. Make the player feel like they've just entered a world of mystery and ancient magic. Include details about what the player can see, hear, and sense around them. End with the current situation, ready for the player's first action."""

        return story_system_prompt, start_message
    
    def truncate_messages(self) -> None:
        """Remove old messages to stay within token limits"""
        if not self.messages or len(self.messages) < 2:
            return
        
        # Estimate token count
        token_counts = [len(message.content.split()) for message in self.messages]
        current_total = sum(token_counts)
        
        # Remove messages from the middle, keeping system message and recent context
        index = 1  # Start after system message
        while current_total > self.config.num_ctx * 0.8 and len(self.messages) > 3:
            if index < len(self.messages) - 1:
                removed_msg = self.messages.pop(index)
                current_total -= len(removed_msg.content.split())
            else:
                break
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within the specified width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            # Handle newlines in the word
            if '\n' in word:
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    if i == 0:
                        test_line = current_line + (' ' if current_line else '') + part
                    else:
                        if current_line:
                            lines.append(current_line)
                            current_line = ""
                        test_line = part
                    
                    if i < len(parts) - 1:  # Not the last part
                        # Check if the line fits before adding it
                        if self.config.font.size(test_line)[0] <= max_width:
                            lines.append(test_line)
                        else:
                            # Break long line into smaller pieces
                            lines.extend(self._break_long_line(test_line, max_width))
                        current_line = ""
                    else:
                        current_line = test_line
            else:
                # Normal word processing
                test_line = current_line + (' ' if current_line else '') + word
                text_width = self.config.font.size(test_line)[0]
                
                if text_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    
                    # Check if the word itself is too long
                    word_width = self.config.font.size(word)[0]
                    if word_width <= max_width:
                        current_line = word
                    else:
                        # Break the long word
                        lines.extend(self._break_long_line(word, max_width))
                        current_line = ""
        
        if current_line:
            # Final check for the last line
            if self.config.font.size(current_line)[0] <= max_width:
                lines.append(current_line)
            else:
                lines.extend(self._break_long_line(current_line, max_width))
        
        return lines
    
    def _break_long_line(self, text: str, max_width: int) -> List[str]:
        """Break a long line that doesn't fit into smaller pieces"""
        if not text:
            return []
        
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            if self.config.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def draw_text_area(self) -> None:
        """Draw the main text area"""
        text_rect = pygame.Rect(
            self.margin, 
            self.margin, 
            self.config.width - 2 * self.margin, 
            self.text_area_height
        )
        
        # Draw background
        pygame.draw.rect(self.screen, self.config.colors['black'], text_rect)
        pygame.draw.rect(self.screen, self.config.colors['dark_green'], text_rect, 2)
          # Calculate text rendering area with more precise margins
        text_margin = 15  # Internal margin for text
        text_width = text_rect.width - (text_margin * 2)  # Account for both sides
        y_pos = text_rect.y + text_margin - self.scroll_offset
        
        # Render messages
        for message in self.display_messages:
            if message['role'] == 'user':
                color = self.config.colors['amber']
                content = f"> {message['content']}"
            else:
                color = self.config.colors['green']
                content = message['content']
              # Wrap and render text
            lines = self.wrap_text(content, text_width)
            for line in lines:
                if y_pos > text_rect.bottom:
                    break
                if y_pos + self.config.line_height > text_rect.y:
                    text_surface = self.config.font.render(line, True, color)
                    self.screen.blit(text_surface, (text_rect.x + text_margin, y_pos))
                y_pos += self.config.line_height
        
        # Auto-scroll if text goes beyond visible area
        max_y = y_pos + self.scroll_offset
        if max_y > text_rect.bottom - self.config.line_height:
            self.scroll_offset = max_y - text_rect.bottom + self.config.line_height * 2
    
    def draw_input_area(self) -> None:
        """Draw the input area"""
        input_rect = pygame.Rect(
            self.margin,
            self.config.height - self.input_height - self.margin,
            self.config.width - 2 * self.margin,
            self.input_height
        )
        
        # Draw background
        pygame.draw.rect(self.screen, self.config.colors['dark_gray'], input_rect)
        pygame.draw.rect(self.screen, self.config.colors['amber'], input_rect, 2)
        
        # Prepare input text with prompt
        prompt = "(update story)> " if self.is_story_update else "> "
        display_text = prompt + self.input_text
        
        # Add cursor if visible
        if self.cursor_visible and not self.is_ai_typing:
            display_text += "_"
        
        # Render text
        text_surface = self.config.font.render(display_text, True, self.config.colors['amber'])
        self.screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
    
    def draw_status_bar(self) -> None:
        """Draw status information"""
        status_text = f"SuperZork | Backend: {self.config.ai_backend.upper()} | Model: {self.config.model} | "
        if self.is_ai_typing:
            status_text += "AI is thinking..."
        else:
            status_text += "Ready"
        
        text_surface = self.config.font.render(status_text, True, self.config.colors['cyan'])
        self.screen.blit(text_surface, (self.margin, 5))
    
    def stream_ai_response(self, message: str):
        """Stream response from AI backend"""
        # Add user message to conversation
        if message.strip():
            self.messages.append(Message("user", message))
        
        try:
            # Stream response from AI client
            for token in self.config.ai_client.stream_chat(self.messages):
                yield token
        except Exception as e:
            print(f"AI Error: {e}")
            yield "The mystical AI oracle has encountered an error. Please try again."
    
    def process_input(self, user_input: str) -> bool:
        """Process user input. Returns True if game should continue."""
        command = user_input.lower().strip()
        
        if command == "quit":
            return False
            
        elif command == "undo":
            if self.is_story_update:
                return True
            
            if len(self.messages) > 1 and self.messages[-1].role == "assistant":
                self.messages.pop()
                if self.display_messages and self.display_messages[-1]["role"] == "assistant":
                    self.display_messages.pop()
                self.is_story_update = True
                return True
            else:
                self.is_story_update = False
                
        elif command == "debug":
            print("\n--- Debug: Conversation History ---")
            for i, msg in enumerate(self.messages):
                print(f"{i+1}. [{msg.role.upper()}]: {msg.content[:100]}...")
            print("--- End Debug ---\n")
            return True
        
        # Handle story update mode
        if self.is_story_update:
            if user_input.strip():
                self.messages.append(Message("assistant", user_input))
                self.display_messages.append({
                    "role": "assistant",
                    "content": f"(Updated Story): {user_input}"
                })
            self.is_story_update = False
            return True
        
        # Normal input processing
        if user_input.strip():
            # Add to display messages
            self.display_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Manage conversation length
            self.truncate_messages()
            
            # Start AI response
            self.text_generator = self.stream_ai_response(user_input)
            self.display_messages.append({
                "role": "assistant",
                "content": ""
            })
            self.is_ai_typing = True
            self.next_word_time = pygame.time.get_ticks() + 100
        
        return True
    
    def update_ai_response(self) -> None:
        """Update AI response streaming"""
        if self.text_generator and pygame.time.get_ticks() > self.next_word_time:
            try:
                next_chunk = next(self.text_generator)
                if self.display_messages:
                    self.display_messages[-1]['content'] += next_chunk
                self.next_word_time = pygame.time.get_ticks() + 50  # Faster typing
            except StopIteration:
                # AI finished responding
                self.text_generator = None
                self.is_ai_typing = False
                
                # Add final response to conversation
                if self.display_messages:
                    self.messages.append(Message("assistant", self.display_messages[-1]['content']))
    
    def load_system_prompt(self) -> str:
        """Load the system prompt from external file"""
        prompt_file = Path("prompts/system_prompt.txt")
        
        if not prompt_file.exists():
            print(f"Error: System prompt file not found: {prompt_file}")
            print("Please ensure the prompts/system_prompt.txt file exists.")
            sys.exit(1)
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error: Could not load system prompt file: {e}")
            sys.exit(1)

    def run(self) -> None:
        """Main game loop"""
        clock = pygame.time.Clock()
        
        try:
            # Initialize the game
            system_prompt, first_message = self.build_story_system_prompt()
            self.messages.append(Message("system", system_prompt))
            
            # Start with the initial story
            self.text_generator = self.stream_ai_response(first_message)
            self.display_messages = [{"role": "assistant", "content": ""}]
            self.is_ai_typing = True
            self.next_word_time = pygame.time.get_ticks() + 500
            
            running = True
            while running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    elif event.type == pygame.KEYDOWN and not self.is_ai_typing:
                        if event.key == pygame.K_RETURN:
                            if self.input_text.strip():
                                if not self.process_input(self.input_text):
                                    running = False
                                self.input_text = ""
                                
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                            
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            
                        else:
                            if event.unicode.isprintable():
                                self.input_text += event.unicode
                
                # Update AI response
                self.update_ai_response()
                
                # Update cursor blinking
                self.cursor_timer += clock.get_time()
                if self.cursor_timer > 500:  # Blink every 500ms
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = 0
                
                # Render everything
                self.screen.fill(self.config.colors['black'])
                self.draw_status_bar()
                self.draw_text_area()
                self.draw_input_area()
                
                pygame.display.flip()
                clock.tick(60)
                
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            pygame.quit()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="SuperZork GUI: AI-Powered Text Adventure Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python superzork_gui.py -s stories/zork_adventure.yaml
  python superzork_gui.py --story stories/custom_adventure.yaml --backend huggingface
  python superzork_gui.py -s stories/huggingface_adventure.yaml -b ollama
        """
    )
    parser.add_argument(
        "-s", "--story",
        required=True,
        help="Path to the YAML story configuration file"
    )
    parser.add_argument(
        "-b", "--backend",
        choices=["ollama", "huggingface"],
        help="AI backend to use (overrides story configuration)"
    )
    
    args = parser.parse_args()
    
    # Show available backends if none are available
    available = get_available_backends()
    if not available:
        print(f"{Fore.RED}No AI backends are available!")
        print(f"{Fore.YELLOW}Please ensure either:")
        print(f"{Fore.YELLOW}  - Ollama is running (install from https://ollama.ai/)")
        print(f"{Fore.YELLOW}  - Hugging Face MCP is installed (pip install mcp)")
        sys.exit(1)
    
    try:
        # Create and run the game
        config = GameConfig(args.story, args.backend)
        game = SuperZorkGUI(config)
        game.run()
    except Exception as e:
        print(f"Failed to start game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
