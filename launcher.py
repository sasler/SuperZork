#!/usr/bin/env python3
"""
SuperZork Launcher
Provides an easy way to start SuperZork adventures
"""

import os
import sys
import argparse
from pathlib import Path


def list_stories():
    """List available story files"""
    stories_dir = Path("stories")
    if not stories_dir.exists():
        print("No stories directory found!")
        return []
    
    story_files = list(stories_dir.glob("*.yaml"))
    return story_files


def print_stories():
    """Print available stories with descriptions"""
    stories = list_stories()
    if not stories:
        print("No story files found in the stories directory.")
        return
    
    print("\nAvailable Adventures:")
    print("=" * 50)
    
    for i, story_file in enumerate(stories, 1):
        name = story_file.stem.replace('_', ' ').title()
        print(f"{i}. {name}")
        print(f"   File: {story_file}")
        print()


def launch_game(story_file, gui=False):
    """Launch the game with the specified story"""
    if gui:
        script = "superzork_gui.py"
    else:
        script = "superzork.py"
    
    if not Path(script).exists():
        print(f"Error: {script} not found!")
        return False
    
    # Launch the game
    os.system(f"python {script} -s {story_file}")
    return True


def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="SuperZork Adventure Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py                    # Interactive mode
  python launcher.py --list             # List available stories
  python launcher.py --gui              # Launch with GUI
  python launcher.py -s custom.yaml     # Launch specific story
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available story files"
    )
    
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Launch with GUI interface"
    )
    
    parser.add_argument(
        "--story", "-s",
        help="Specify story file to launch"
    )
    
    args = parser.parse_args()
    
    # Handle list command
    if args.list:
        print_stories()
        return
    
    # Handle specific story launch
    if args.story:
        if not Path(args.story).exists():
            print(f"Error: Story file '{args.story}' not found!")
            sys.exit(1)
        
        launch_game(args.story, args.gui)
        return
    
    # Interactive mode
    print("SuperZork Adventure Launcher")
    print("=" * 40)
    
    stories = list_stories()
    if not stories:
        print("No story files found!")
        return
    
    # Show available stories
    print("\nSelect an adventure:")
    for i, story_file in enumerate(stories, 1):
        name = story_file.stem.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    # Get user choice
    try:
        choice = input(f"\nEnter choice (1-{len(stories)}): ").strip()
        story_index = int(choice) - 1
        
        if 0 <= story_index < len(stories):
            selected_story = stories[story_index]
            
            # Ask about interface
            interface = input("Choose interface (t)erminal or (g)ui [t]: ").strip().lower()
            use_gui = interface.startswith('g')
            
            print(f"\nLaunching {selected_story.name}...")
            launch_game(selected_story, use_gui)
        else:
            print("Invalid choice!")
    
    except (ValueError, KeyboardInterrupt):
        print("\nExiting launcher.")


if __name__ == "__main__":
    main()
