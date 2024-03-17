#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    sudo apt-get update
    sudo apt-get install python3 -y
fi

# Check if Pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Pip is not installed. Installing Pip..."
    sudo apt-get install python3-pip -y
fi

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Run cronjob.py
echo "Running cronjob.py..."
python3 cronjob.py &

# Run discord_bot.py in a separate Python instance
echo "Running discord_bot.py in a separate Python instance..."
cd discord_bot
python3 discord_bot.py &