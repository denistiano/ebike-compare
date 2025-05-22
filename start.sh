#!/bin/bash

# E-Bike Compare Startup Script

# Change to the project directory
cd "$(dirname "$0")"

# Print banner
echo "====================================================="
echo "  E-Bike Compare - Starting up"
echo "====================================================="

# Update conda itself
echo "Updating conda..."
conda update -n base -c defaults conda -y

# Check if conda environment exists, create if not
ENV_NAME="ebike-compare"
if ! conda env list | grep -q "^$ENV_NAME "; then
    echo "Creating conda environment '$ENV_NAME'..."
    conda create -n $ENV_NAME python=3.9 -y
    echo "Conda environment created."
fi

# Activate conda environment
echo "Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# Update all conda packages in the environment
echo "Updating conda packages..."
conda update --all -y

# Install/Update core numeric packages first to ensure compatibility
echo "Installing/updating core numeric packages..."
conda install -y numpy
conda install -y pandas

# Install/Update other dependencies
echo "Updating pip..."
pip install --upgrade pip

echo "Updating project dependencies..."
pip install --upgrade -r requirements.txt

# Verify numpy and pandas compatibility
echo "Verifying package compatibility..."
python -c "import numpy; import pandas; print(f'numpy version: {numpy.__version__}'); print(f'pandas version: {pandas.__version__}')"

# Create data directories if they don't exist
mkdir -p data/current data/archive

# Run the crawler to collect initial data
echo "====================================================="
echo "  Running crawler to collect data"
echo "====================================================="
python -m crawler.crawler

# Start the web application
echo "====================================================="
echo "  Starting web application"
echo "  Access at http://127.0.0.1:5000/"
echo "====================================================="
python -m webapp.app 