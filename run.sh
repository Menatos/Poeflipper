#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    sudo apt-get update
    sudo apt-get install python3 -y
fi

mkdir logs
sudo apt-get install screen -y

# Check if Pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Pip is not installed. Installing Pip..."
    sudo apt-get install python3-pip -y
fi

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

nohup sudo python3 database/initial_create_database.py > /dev/null 2>&1 &
nohup sudo python3 cronjob.py > /dev/null 2>&1 &
nohup sudo python3 discord_bot/discord_bot.py > /dev/null 2>&1 &