#!/bin/bash

# DSA Commiter Installation Script
# This script installs the dsa-commiter CLI tool

set -e  # Exit on any error

echo "🚀 DSA Commiter Installation Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi
print_success "pip3 found"

# Check if git is installed
print_status "Checking Git installation..."
if ! command -v git &> /dev/null; then
    print_warning "Git is not installed. DSA Commiter requires Git for version control features."
    echo "Please install Git: https://git-scm.com/downloads"
else
    print_success "Git found"
fi

# Create virtual environment (optional but recommended)
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Using existing venv."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_status "Installing dependencies..."
pip3 install rich>=12.0.0
print_success "Dependencies installed"

# Install the package in development mode
print_status "Installing dsa-commiter..."
if [ -f "setup.py" ]; then
    pip3 install -e .
    print_success "dsa-commiter installed in editable mode"
else
    print_error "setup.py not found. Make sure you're in the correct directory."
    exit 1
fi

# Verify installation
print_status "Verifying installation..."
if command -v dsa-commiter &> /dev/null; then
    print_success "DSA Commiter installed successfully!"
    echo ""
    echo "🎉 Installation Complete!"
    echo "========================"
    echo ""
    echo "You can now use 'dsa-commiter' command from within the virtual environment."
    echo "Activate the virtual environment with: source venv/bin/activate"
    echo ""
    echo "Usage:"
    echo "  source venv/bin/activate"
    echo "  cd your-project-directory"
    echo "  dsa-commiter"
    echo ""
else
    print_warning "Installation completed but 'dsa-commiter' command not found in PATH."
    echo "You may need to:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Run: python3 -m dsa_commiter.cli_interface"
    echo "3. Ensure pip's bin directory is in your PATH"
fi

print_status "Installation script completed!"