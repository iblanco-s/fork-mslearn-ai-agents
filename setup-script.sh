#!/bin/bash

echo "================================================"
echo "AI Agents Lab Setup Script (Linux)"
echo "================================================"
echo ""

# Install Azure CLI
echo "Installing Azure CLI..."
echo "------------------------------------------------"
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

echo ""
echo "Verifying Azure CLI installation..."
if command -v az &> /dev/null; then
    echo "✓ Azure CLI is installed"
    az version
else
    echo "⚠ Azure CLI not found in PATH. Please install it manually or restart your terminal."
fi

echo ""
echo "------------------------------------------------"

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "✓ Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "------------------------------------------------"

# Install Python dependencies
echo "Installing Python dependencies..."
echo ""

if [ -f "requirements.txt" ]; then
    echo "Installing from consolidated requirements.txt..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ All Python dependencies installed successfully!"
    else
        echo ""
        echo "✗ Failed to install some dependencies. Please check the error messages above."
        exit 1
    fi
else
    echo "✗ requirements.txt not found in the current directory."
    exit 1
fi

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Run 'az login' to authenticate with Azure"
echo "2. Configure your .env files in the respective labfile directories"
echo "3. Start working on the labs!"
echo ""

