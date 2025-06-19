#!/usr/bin/env python3
"""
SuperZork Installation and Setup Script
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and report success/failure"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def check_ollama():
    """Check if Ollama is available"""
    print("🔍 Checking Ollama availability...")
    try:
        result = subprocess.run("ollama --version", shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Ollama found: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Ollama not found or not accessible")
        print("   Please install Ollama from https://ollama.ai/")
        return False


def install_dependencies():
    """Install Python dependencies"""
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )


def check_phi4_mini():
    """Check if phi4-mini model is available in Ollama"""
    print("🔍 Checking for phi4-mini model...")
    try:
        result = subprocess.run("ollama list", shell=True, check=True, capture_output=True, text=True)
        if "phi4-mini" in result.stdout:
            print("✅ phi4-mini model found")
            return True
        else:
            print("⚠️  phi4-mini model not found")
            return False
    except subprocess.CalledProcessError:
        print("❌ Could not check Ollama models")
        return False


def install_phi4_mini():
    """Install phi4-mini model"""
    print("📥 Installing phi4-mini model (this may take a while)...")
    return run_command(
        "ollama pull phi4-mini",
        "Downloading phi4-mini model"
    )


def test_installation():
    """Test the installation by running a simple query"""
    print("🧪 Testing installation...")
    test_story = Path("stories/zork_adventure.yaml")
    
    if not test_story.exists():
        print("❌ Test story file not found")
        return False
    
    # Try to import required modules
    try:
        import yaml
        import requests
        import colorama
        import pygame
        print("✅ All required modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("✅ Installation test passed")
    return True


def main():
    """Main setup function"""
    print("🚀 SuperZork Installation and Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check Ollama
    ollama_available = check_ollama()
    if not ollama_available:
        success = False
    
    # Install Python dependencies
    if not install_dependencies():
        success = False
    
    # Check and install phi4-mini model
    if ollama_available:
        if not check_phi4_mini():
            print("\n🤖 phi4-mini model not found. Would you like to install it?")
            choice = input("Install phi4-mini? (y/n) [y]: ").strip().lower()
            
            if choice != 'n':
                if not install_phi4_mini():
                    print("⚠️  Failed to install phi4-mini model")
                    print("   You can install it manually later with: ollama pull phi4-mini")
    
    # Test installation
    if success:
        if test_installation():
            print("\n🎉 Installation completed successfully!")
            print("\n📖 Quick Start:")
            print("   python launcher.py           # Interactive launcher")
            print("   python superzork.py -s stories/zork_adventure.yaml")
            print("   python superzork_gui.py -s stories/zork_adventure.yaml")
        else:
            print("\n⚠️  Installation completed with warnings")
            print("   Some components may not work correctly")
    else:
        print("\n❌ Installation failed")
        print("   Please resolve the issues above and try again")
    
    print("\n🔗 For help and documentation, see README.md")


if __name__ == "__main__":
    main()
