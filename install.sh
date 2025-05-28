
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
print_status "Setting up installation..."

# Install the package
print_status "Installing dsa-commiter..."

# Install dependencies first
pip3 install rich>=12.0.0

# Install the package in development mode if setup.py exists
if [ -f "setup.py" ]; then
    print_status "Installing from source..."
    pip3 install -e .
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
    echo "You can now use 'dsa-commiter' command from anywhere in your terminal."
    echo ""
    echo "Usage:"
    echo "  dsa-commiter    - Start the interactive CLI"
    echo ""
    echo "Example:"
    echo "  cd your-project-directory"
    echo "  dsa-commiter"
    echo ""
else
    print_warning "Installation completed but 'dsa-commiter' command not found in PATH."
    echo "You may need to:"
    echo "1. Restart your terminal"
    echo "2. Add pip's bin directory to your PATH"
    echo "3. Or run: python3 -m dsa_commiter.cli_interface"
fi

print_status "Installation script completed!"