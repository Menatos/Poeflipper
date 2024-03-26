#!/bin/bash

# Define constants
RELEASE_BRANCH='Release-1.0_3.24'
RUN_SCRIPT='run.sh'

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Function to stop python processes
stop_python_processes() {
    echo "Stopping all running python processes"
    pkill -9 -f "python" || handle_error "Failed to stop python processes"
    echo "Python processes stopped"
}

# Function to fetch and checkout release branch
fetch_checkout_release_branch() {
    echo "Fetching and checking out release branch: $RELEASE_BRANCH"
    git fetch || handle_error "Failed to fetch from repository"
    git checkout "$RELEASE_BRANCH" || handle_error "Failed to checkout $RELEASE_BRANCH"
    echo "Checked out release branch: $RELEASE_BRANCH"
}

# Function to pull changes
pull_changes() {
    echo "Pulling changes from release branch: $RELEASE_BRANCH"
    git pull || handle_error "Failed to pull changes"
    echo "Pulled changes from release branch: $RELEASE_BRANCH"
}

# Function to execute run.sh
execute_run_script() {
    echo "Executing $RUN_SCRIPT to start processes"
    sudo bash "$RUN_SCRIPT" || handle_error "Failed to execute $RUN_SCRIPT"
    echo "$RUN_SCRIPT started"
}

# Main script
echo "---- Starting Script ----"
stop_python_processes
fetch_checkout_release_branch
pull_changes
execute_run_script
echo "Script successfully completed"
echo "---- HAVE A NICE DAY ----"