
@echo off
echo 🚀 DSA Commiter Installation Script
echo ==================================

REM Colors (not supported in all terminals, fallback to plain echo)
set GREEN=[SUCCESS]
set RED=[ERROR]
set YELLOW=[WARNING]
set BLUE=[INFO]

REM Check for Python
echo %BLUE% Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED% Python not found. Please install Python 3.7+ from https://www.python.org/downloads/
    exit /b 1
)
echo %GREEN% Python found

REM Check for pip
echo %BLUE% Checking pip installation...
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED% pip not found. Please install pip.
    exit /b 1
)
echo %GREEN% pip found

REM Check for Git
echo %BLUE% Checking Git installation...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW% Git not found. Please install Git from https://git-scm.com/downloads
) else (
    echo %GREEN% Git found
)

REM Create virtual environment
echo %BLUE% Creating virtual environment...
if exist venv (
    echo %YELLOW% Virtual environment already exists.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo %RED% Failed to create virtual environment.
        exit /b 1
    )
    echo %GREEN% Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo %RED% Failed to activate virtual environment
    exit /b 1
)
echo %GREEN% Virtual environment activated

REM Install dependencies
echo %BLUE% Installing dependencies...
pip install rich>=12.0.0
if errorlevel 1 (
    echo %RED% Failed to install dependencies
    exit /b 1
)
echo %GREEN% Dependencies installed

REM Install package in development mode
echo %BLUE% Installing dsa-commiter...
if exist setup.py (
    pip install -e .
    echo %GREEN% dsa-commiter installed in editable mode
) else (
    echo %RED% setup.py not found. Make sure you're in the correct directory.
    exit /b 1
)

REM Final usage message
echo.
echo %GREEN% Installation Complete!
echo ========================
echo To use the CLI:
echo     1. Activate venv: venv\Scripts\activate
echo     2. Run: dsa-commiter
echo If command not found, try: python -m dsa_commiter.cli_interface
echo.

exit /b 0
