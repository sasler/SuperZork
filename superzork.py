#!/usr/bin/env python3
"""
SuperZork: AI-Powered Text Adventure Game
Terminal Version

A classic text adventure game enhanced with AI using Ollama and phi4-mini.
Inspired by the legendary Zork series.
"""

import requests
import json
import yaml
import argparse
import sys
import os
from pathlib import Path
from typing import Iterator, Any, TypedDict, List
from colorama import Fore, init, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class Message(TypedDict):
    """Type definition for chat messages"""
    role: str
    content: str


class SuperZorkGame:
    """Main game class for the terminal version"""
    
    def __init__(self, story_file: str):
        """Initialize the game with a story configuration file"""
        self.messages: List[Message] = []
        self.load_config(story_file)
        self.print_welcome()
    
    def load_config(self, story_file: str) -> None:
        """Load game configuration from YAML file"""
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Ollama configuration
            self.model = config.get('model', 'phi4-mini')
            self.ollama_url = config.get('ollama_url', 'http://localhost:11434')
            self.num_ctx = config.get('num_tokens', 4096)
            self.temperature = config.get('temperature', 0.7)
            
            # Story elements
            self.player_card = config.get('player_card', '')
            self.companion_cards = config.get('companion_cards', [])
            self.story_card = config.get('story_card', '')
            
            if not self.story_card:
                raise ValueError("Story card is required but not found in configuration")
                
        except FileNotFoundError:
            self.color_print("Error: Story file not found!", Fore.RED)
            sys.exit(1)
        except yaml.YAMLError as exc:
            self.color_print(f"Error parsing YAML file: {exc}", Fore.RED)
            sys.exit(1)
        except Exception as e:
            self.color_print(f"Configuration error: {e}", Fore.RED)
            sys.exit(1)
    
    def print_welcome(self) -> None:
        """Print the game welcome message"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=" * 60)
        print(f"{Fore.CYAN}{Style.BRIGHT}    SUPERZORK: THE GREAT UNDERGROUND EMPIRE AWAKENS")
        print(f"{Fore.CYAN}{Style.BRIGHT}=" * 60)
        print(f"{Fore.YELLOW}Welcome to SuperZork! An AI-powered text adventure.")
        print(f"{Fore.YELLOW}Type your actions naturally. The AI will respond dynamically.")
        print(f"{Fore.MAGENTA}Commands: 'quit' to exit, 'undo' to modify story, 'debug' for history, 'help' for help")
        print(f"{Fore.CYAN}=" * 60 + Style.RESET_ALL)
    
    def color_print(self, message: str, color: str = Fore.WHITE) -> None:
        """Print a colored message"""
        print(color + message + Style.RESET_ALL)
    
    def load_system_prompt(self) -> str:
        """Load the system prompt from external file"""
        prompt_file = Path("prompts/system_prompt.txt")
        
        if not prompt_file.exists():
            self.color_print(f"Error: System prompt file not found: {prompt_file}", Fore.RED)
            self.color_print("Please ensure the prompts/system_prompt.txt file exists.", Fore.YELLOW)
            sys.exit(1)
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            self.color_print(f"Error: Could not load system prompt file: {e}", Fore.RED)
            sys.exit(1)
    
    def build_story_system_prompt(self) -> tuple[str, str]:
        """Build the initial system prompt and first message"""
        story_system_prompt = self.load_system_prompt()

        companions_str = '\n'.join(self.companion_cards)
        start_message = f"""Initialize the SuperZork adventure using the following information:

STORY SETTING:
```
{self.story_card}
```

PLAYER CHARACTER:
```
{self.player_card}
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
        
        # Estimate token count (rough approximation)
        token_counts = [len(message['content'].split()) for message in self.messages]
        current_total = sum(token_counts)
          # Remove messages from the middle, keeping system message and recent context
        index = 1  # Start after system message
        while current_total > self.num_ctx * 0.8 and len(self.messages) > 3:
            if index < len(self.messages) - 1:  # Don't remove the last message
                removed_msg = self.messages.pop(index)
                current_total -= len(removed_msg['content'].split())
            else:
                break
    
    def stream_llm_chat(self, message: str) -> Iterator[str]:
        """Stream response from Ollama LLM"""
        # Add user message to conversation
        if message.strip():  # Only add non-empty messages
            self.messages.append({
                "role": "user",
                "content": message
            })
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": True,
            "options": {
                "num_ctx": self.num_ctx,
                "temperature": self.temperature,
            }
        }
        
        try:
            # Increase timeout and add connection timeout
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                stream=True,
                timeout=(10, 120)  # (connection timeout, read timeout)
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line)
                        if 'message' in json_data and 'content' in json_data['message']:
                            content = json_data['message']['content']
                            if content:
                                yield content
                        # Check if we've reached the end of the response
                        if json_data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.Timeout:
            self.color_print("Request timed out. The AI is taking longer than expected.", Fore.YELLOW)
            yield "The ancient spirits are taking their time to respond... Perhaps try a simpler command or restart the game if this persists."
        except requests.exceptions.ConnectionError:
            self.color_print("Could not connect to Ollama. Make sure it's running.", Fore.RED)
            yield "The magical connection to the underground realm has been severed. Please ensure Ollama is running and try again."
        except requests.exceptions.RequestException as e:
            self.color_print(f"Error connecting to Ollama: {e}", Fore.RED)
            self.color_print("Make sure Ollama is running and phi4-mini model is available.", Fore.YELLOW)
            yield "The mystical AI oracle has encountered an error. Please check your connection and try again."
    
    def handle_special_commands(self, user_input: str) -> bool:
        """Handle special game commands. Returns True if command was handled."""
        command = user_input.lower().strip()
        
        if command == "quit":
            self.color_print("\n" + "=" * 50, Fore.CYAN)
            self.color_print("Thanks for playing SuperZork!", Fore.YELLOW)
            self.color_print("The Great Underground Empire awaits your return...", Fore.CYAN)
            self.color_print("=" * 50, Fore.CYAN)
            return True
            
        elif command == "undo":
            if len(self.messages) > 1 and self.messages[-1]["role"] == "assistant":
                self.messages.pop()
                self.color_print("\n--- Story Modification Mode ---", Fore.MAGENTA)
                self.color_print("How would you like to change what just happened?", Fore.YELLOW)
                updated_story = input(f"{Fore.MAGENTA}(story update)> {Style.RESET_ALL}")
                
                if updated_story.strip():
                    new_message = {
                        "role": "assistant",
                        "content": updated_story
                    }
                    self.messages.append(new_message)
                    self.color_print(f"\n{Fore.BLUE}Story updated: {updated_story}{Style.RESET_ALL}")
                else:
                    self.color_print("No changes made.", Fore.YELLOW)
            else:
                self.color_print("Nothing to undo.", Fore.RED)
            return False
            
        elif command == "debug":
            self.color_print("\n--- Debug: Conversation History ---", Fore.MAGENTA)
            for i, msg in enumerate(self.messages):
                role_color = Fore.GREEN if msg['role'] == 'user' else Fore.BLUE if msg['role'] == 'assistant' else Fore.CYAN
                self.color_print(f"{i+1}. [{msg['role'].upper()}]: {msg['content'][:100]}...", role_color)
            self.color_print("--- End Debug ---\n", Fore.MAGENTA)
            return False
            
        elif command == "help":
            self.print_help()
            return False
            
        return False
    
    def print_help(self) -> None:
        """Print help information"""
        self.color_print("\n--- SuperZork Help ---", Fore.CYAN)
        self.color_print("Available Commands:", Fore.YELLOW)
        self.color_print("• quit - Exit the game", Fore.WHITE)
        self.color_print("• undo - Modify the last AI response", Fore.WHITE)
        self.color_print("• debug - Show conversation history", Fore.WHITE)
        self.color_print("• help - Show this help message", Fore.WHITE)
        self.color_print("\nGameplay Tips:", Fore.YELLOW)
        self.color_print("• Type actions naturally: 'go north', 'examine door', 'take lamp'", Fore.WHITE)
        self.color_print("• Be creative! The AI responds to unexpected actions", Fore.WHITE)
        self.color_print("• Classic adventure commands work: look, inventory, use, etc.", Fore.WHITE)
        self.color_print("• Pay attention to descriptions for clues and hidden details", Fore.WHITE)
        self.color_print("--- End Help ---\n", Fore.CYAN)
    
    def run(self) -> None:
        """Main game loop"""
        try:
            # Initialize the game with system prompt
            system_prompt, first_message = self.build_story_system_prompt()
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
            
            # Get initial story description
            self.color_print("\nInitializing the Great Underground Empire...\n", Fore.YELLOW)
            
            response_text = ""
            for token in self.stream_llm_chat(first_message):
                print(f"{Fore.BLUE}{token}{Style.RESET_ALL}", end="", flush=True)
                response_text += token
            
            # Add AI response to conversation
            if response_text:
                self.messages.append({
                    "role": "assistant", 
                    "content": response_text
                })
            
            print("\n")  # Add newline after initial response
            
            # Main game loop
            while True:
                try:
                    user_input = input(f"\n{Fore.GREEN}> {Style.RESET_ALL}").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if self.handle_special_commands(user_input):
                        break
                    
                    # Manage conversation length
                    self.truncate_messages()
                    
                    # Get AI response
                    response_text = ""
                    for token in self.stream_llm_chat(user_input):
                        print(f"{Fore.BLUE}{token}{Style.RESET_ALL}", end="", flush=True)
                        response_text += token
                    
                    # Add AI response to conversation
                    if response_text:
                        self.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })
                    
                    print()  # Add newline after response
                    
                except KeyboardInterrupt:
                    self.color_print("\n\nGame interrupted. The empire fades into darkness...", Fore.YELLOW)
                    break
                except EOFError:
                    self.color_print("\n\nInput ended. Farewell, adventurer!", Fore.YELLOW)
                    break
                    
        except Exception as e:
            self.color_print(f"\nAn unexpected error occurred: {e}", Fore.RED)
            self.color_print("The ancient magic has become unstable. Please restart your adventure.", Fore.YELLOW)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="SuperZork: AI-Powered Text Adventure Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python superzork.py -s stories/zork_adventure.yaml
  python superzork.py --story stories/custom_adventure.yaml
        """
    )
    parser.add_argument(
        "-s", "--story",
        required=True,
        help="Path to the YAML story configuration file"
    )
    
    args = parser.parse_args()
    
    # Create and run the game
    game = SuperZorkGame(args.story)
    game.run()


if __name__ == "__main__":
    main()
