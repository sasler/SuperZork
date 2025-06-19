#!/usr/bin/env python3
"""
SuperZork Configuration Validator
Validates YAML story configuration files
"""

import yaml
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List


class ConfigValidator:
    """Validates SuperZork story configuration files"""
    
    REQUIRED_FIELDS = [
        'model',
        'story_card',
        'player_card'
    ]
    
    OPTIONAL_FIELDS = [
        'ollama_url',
        'num_tokens', 
        'temperature',
        'companion_cards'
    ]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_file(self, file_path: Path) -> bool:
        """Validate a single configuration file"""
        self.errors = []
        self.warnings = []
        
        if not file_path.exists():
            self.errors.append(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"File reading error: {e}")
            return False
        
        if not isinstance(config, dict):
            self.errors.append("Configuration must be a YAML dictionary")
            return False
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in config:
                self.errors.append(f"Missing required field: {field}")
            elif not config[field] or not config[field].strip():
                self.errors.append(f"Required field is empty: {field}")
        
        # Validate specific fields
        self._validate_model(config.get('model'))
        self._validate_numeric_fields(config)
        self._validate_text_fields(config)
        self._validate_companion_cards(config.get('companion_cards'))
        
        return len(self.errors) == 0
    
    def _validate_model(self, model: Any) -> None:
        """Validate model field"""
        if not model:
            return
        
        if not isinstance(model, str):
            self.errors.append("Model must be a string")
            return
        
        common_models = [
            'phi4-mini', 'llama2', 'llama3', 'mistral', 'gemma',
            'codellama', 'vicuna', 'orca-mini'
        ]
        
        if model not in common_models:
            self.warnings.append(f"Uncommon model '{model}' - ensure it's available in Ollama")
    
    def _validate_numeric_fields(self, config: Dict[str, Any]) -> None:
        """Validate numeric configuration fields"""
        numeric_fields = {
            'num_tokens': (512, 32768, "Context length"),
            'temperature': (0.0, 2.0, "Temperature")
        }
        
        for field, (min_val, max_val, description) in numeric_fields.items():
            value = config.get(field)
            if value is None:
                continue
            
            if not isinstance(value, (int, float)):
                self.errors.append(f"{field} must be a number")
                continue
            
            if not (min_val <= value <= max_val):
                self.warnings.append(
                    f"{field} ({value}) outside recommended range {min_val}-{max_val}"
                )
    
    def _validate_text_fields(self, config: Dict[str, Any]) -> None:
        """Validate text content fields"""
        text_fields = ['story_card', 'player_card']
        
        for field in text_fields:
            value = config.get(field)
            if not value:
                continue
            
            if not isinstance(value, str):
                self.errors.append(f"{field} must be a string")
                continue
            
            # Check length
            if len(value.strip()) < 50:
                self.warnings.append(f"{field} is quite short (< 50 characters)")
            elif len(value) > 2000:
                self.warnings.append(f"{field} is very long (> 2000 characters)")
    
    def _validate_companion_cards(self, companions: Any) -> None:
        """Validate companion cards field"""
        if companions is None:
            return
        
        if not isinstance(companions, list):
            self.errors.append("companion_cards must be a list")
            return
        
        for i, companion in enumerate(companions):
            if not isinstance(companion, str):
                self.errors.append(f"Companion card {i+1} must be a string")
                continue
            
            if len(companion.strip()) < 30:
                self.warnings.append(f"Companion card {i+1} is quite short")
    
    def print_results(self, file_path: Path) -> None:
        """Print validation results"""
        print(f"\nValidation Results for: {file_path}")
        print("=" * 50)
        
        if not self.errors and not self.warnings:
            print("✅ Configuration is valid!")
            return
        
        if self.errors:
            print(f"❌ Errors ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"⚠️  Warnings ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.errors:
            print("\n✅ Configuration is valid (with warnings)")
        else:
            print(f"\n❌ Configuration has {len(self.errors)} error(s)")


def validate_all_stories():
    """Validate all story files in the stories directory"""
    stories_dir = Path("stories")
    if not stories_dir.exists():
        print("Stories directory not found!")
        return False
    
    story_files = list(stories_dir.glob("*.yaml"))
    if not story_files:
        print("No YAML files found in stories directory!")
        return False
    
    validator = ConfigValidator()
    all_valid = True
    
    print(f"Found {len(story_files)} story files to validate:")
    
    for story_file in story_files:
        is_valid = validator.validate_file(story_file)
        validator.print_results(story_file)
        
        if not is_valid:
            all_valid = False
        
        print()  # Add spacing between files
    
    return all_valid


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="SuperZork Configuration Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_config.py                              # Validate all stories
  python validate_config.py -f stories/zork_adventure.yaml  # Validate specific file
        """
    )
    
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="Validate a specific configuration file"
    )
    
    args = parser.parse_args()
    
    if args.file:
        # Validate single file
        validator = ConfigValidator()
        is_valid = validator.validate_file(args.file)
        validator.print_results(args.file)
        
        if not is_valid:
            sys.exit(1)
    else:
        # Validate all stories
        if not validate_all_stories():
            sys.exit(1)
    
    print("\n🎉 Validation completed!")


if __name__ == "__main__":
    main()
