@echo off
echo SuperZork Setup Script
echo =====================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Checking Ollama installation...
ollama --version
if errorlevel 1 (
    echo ERROR: Ollama not found! Please install Ollama from https://ollama.ai/
    pause
    exit /b 1
)

echo.
echo Checking for phi4-mini model...
ollama list | findstr "phi4-mini"
if errorlevel 1 (
    echo phi4-mini model not found. Installing...
    echo This may take a while...
    ollama pull phi4-mini
) else (
    echo phi4-mini model already installed.
)

echo.
echo Setup complete! 
echo.
echo To start SuperZork:
echo   python launcher.py
echo   python superzork.py -s stories/zork_adventure.yaml
echo   python superzork_gui.py -s stories/zork_adventure.yaml
echo.
pause
