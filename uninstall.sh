
#!/bin/bash

# DSA Commiter Uninstallation Script

echo "🗑️  DSA Commiter Uninstallation Script"
echo "====================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

print_status "Uninstalling dsa-commiter..."

# Uninstall the package
if pip3 show dsa-commiter &> /dev/null; then
    pip3 uninstall dsa-commiter -y
    print_success "DSA Commiter uninstalled successfully!"
else
    print_warning "DSA Commiter package not found in pip."
fi

# Remove any remaining files if installed in development mode
if [ -f "setup.py" ]; then
    print_status "Cleaning up development installation..."
    pip3 uninstall dsa-commiter -y 2>/dev/null || true
fi

# Check if command still exists
if command -v dsa-commiter &> /dev/null; then
    print_warning "Command 'dsa-commiter' still exists. You may need to restart your terminal."
else
    print_success "Command 'dsa-commiter' removed successfully!"
fi

print_status "Uninstallation completed!"
echo "Thank you for using DSA Commiter! 👋"