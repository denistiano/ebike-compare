#!/bin/bash

# Combined E-Bike Compare Startup Script

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

# Function to check if the web server is running
check_webapp_running() {
    # Try to connect to the web server
    if curl -s http://127.0.0.1:5000/ > /dev/null; then
        return 0  # Server is running
    else
        return 1  # Server is not running
    fi
}

# Function to run the crawler
run_crawler() {
    echo "====================================================="
    echo "  Running crawler to collect data at $(date)"
    echo "====================================================="
    python -m crawler.crawler
}

# Function for periodic crawler execution
schedule_crawler() {
    while true; do
        # Sleep for 1 minute (1*60=60 seconds)
        # Sleep for 5 minutes (5*60=300 seconds)
        # Sleep for 10 minutes (10*60=600 seconds)
        # Sleep for 30 minutes (30*60=1800 seconds)
        # Sleep for 1 hour (1*60*60=3600 seconds)
        # Sleep for 8 hours (8*60*60=28800 seconds)
        sleep 1800
        run_crawler
    done
}

# Start the web application in the background
echo "====================================================="
echo "  Starting web application"
echo "  Access at http://127.0.0.1:5000/"
echo "====================================================="
python -m webapp.app &
WEBAPP_PID=$!

# Wait for web server to be ready
echo "Waiting for web server to start..."
max_attempts=30
attempts=0
while ! check_webapp_running && [ $attempts -lt $max_attempts ]; do
    echo "Waiting for web server (attempt $((attempts+1))/$max_attempts)..."
    sleep 1
    attempts=$((attempts+1))
done

if check_webapp_running; then
    echo "Web server is running!"
    
    # Run crawler for the first time
    run_crawler
    
    # Start recurring crawler in the background
    echo "====================================================="
    echo "  Starting recurring crawler (every 8 hours)"
    echo "  First run completed, next run in 8 hours"
    echo "====================================================="
    schedule_crawler &
    SCHEDULER_PID=$!
    
    # Wait for the webapp process
    echo "Web application is running. Press Ctrl+C to exit."
    wait $WEBAPP_PID
else
    echo "Web server failed to start within the timeout period."
    exit 1
fi 