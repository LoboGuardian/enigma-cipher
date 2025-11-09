#!/bin/bash
# Enigma Cipher - Setup Script
# Automatically installs dependencies and launches the GUI

echo "=================================="
echo "  Enigma M3 - Setup Script"
echo "=================================="
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed."
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo ""
    echo "Please restart your terminal and run this script again."
    exit 1
fi

echo "✓ Poetry found"
echo ""

# Check Python version
PYTHON_VERSION=$(poetry run python --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "Python version: $PYTHON_VERSION"
echo ""

# Install dependencies
echo "Installing dependencies..."
poetry install

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully"
    echo ""
    echo "=================================="
    echo "  Setup Complete!"
    echo "=================================="
    echo ""
    echo "To run the GUI:"
    echo "  poetry run python run_gui.py"
    echo ""
    echo "To run the CLI:"
    echo "  poetry run python main.py"
    echo ""
    echo "Would you like to launch the GUI now? (y/n)"
    read -r response

    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo ""
        echo "Launching Enigma GUI..."
        poetry run python run_gui.py
    else
        echo ""
        echo "Setup complete. Run 'poetry run python run_gui.py' when ready."
    fi
else
    echo ""
    echo "✗ Error installing dependencies"
    echo "Please check the error messages above."
    exit 1
fi
