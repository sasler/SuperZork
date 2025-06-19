#!/usr/bin/env python3
"""
Test script for SuperZork to verify all components work correctly.
"""

import os
import sys
import yaml
from pathlib import Path

def test_imports():
    """Test that all modules import correctly."""
    print("🧪 Testing imports...")
    
    try:
        from superzork import SuperZorkGame
        print("✅ Terminal version imports successfully")
    except Exception as e:
        print(f"❌ Terminal version import failed: {e}")
        return False
    
    try:
        from superzork_gui import SuperZorkGUI
        print("✅ GUI version imports successfully")
    except Exception as e:
        print(f"❌ GUI version import failed: {e}")
        return False
    
    return True

def test_system_prompt():
    """Test that system prompt loading works."""
    print("\n🧪 Testing system prompt loading...")
    
    try:
        from superzork import SuperZorkGame
        game = SuperZorkGame('stories/zork_adventure.yaml')
        prompt = game.load_system_prompt()
        
        if len(prompt) > 100:
            print(f"✅ System prompt loaded successfully ({len(prompt)} characters)")
            return True
        else:
            print(f"❌ System prompt too short ({len(prompt)} characters)")
            return False
    except Exception as e:
        print(f"❌ System prompt loading failed: {e}")
        return False

def test_story_files():
    """Test that story files are valid YAML."""
    print("\n🧪 Testing story files...")
    
    stories_dir = Path('stories')
    if not stories_dir.exists():
        print("❌ Stories directory not found")
        return False
    
    story_files = list(stories_dir.glob('*.yaml'))
    if not story_files:
        print("❌ No story files found")
        return False
    
    all_valid = True
    for story_file in story_files:
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✅ {story_file.name} is valid YAML")
        except Exception as e:
            print(f"❌ {story_file.name} is invalid: {e}")
            all_valid = False
    
    return all_valid

def test_config_validation():
    """Test configuration validation."""
    print("\n🧪 Testing configuration validation...")
    
    try:
        from validate_config import ConfigValidator
        
        # Test with a known good config
        story_file = Path('stories/zork_adventure.yaml')
        if story_file.exists():
            validator = ConfigValidator()
            is_valid = validator.validate_file(story_file)
            if is_valid:
                print(f"✅ Configuration validation works")
                return True
            else:
                print(f"❌ Configuration validation failed: {validator.errors}")
                return False
        else:
            print(f"❌ Test story file not found: {story_file}")
            return False
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 SuperZork System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_system_prompt,
        test_story_files,
        test_config_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SuperZork is ready to play!")
        print("\nTo start the game:")
        print("  Terminal: python superzork.py")
        print("  GUI:      python superzork_gui.py")
        print("  Launcher: python launcher.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
