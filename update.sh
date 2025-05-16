#!/bin/bash

# Yes I used AI to generate this file. I have no interest in learning linux bash
# Configuration
PYTHON_SCRIPT="/path/to/your/script.py"  # Replace with your script's path
PID_FILE="/tmp/your_script.pid"       # File to store the process ID


# Function to start the Python script
start_script() {
  if [ -f "$PID_FILE" ]; then
    echo "Script already running. PID found in $PID_FILE."
    return 1 # Indicate failure
  fi
  
  echo "Starting $PYTHON_SCRIPT..."
  nohup python "$PYTHON_SCRIPT" > /dev/null 2>&1 &
  echo $! > "$PID_FILE"
  echo "Script started. PID saved to $PID_FILE."
  return 0 # Indicate success
}


# Function to stop the Python script
stop_script() {
  if [ ! -f "$PID_FILE" ]; then
    echo "No PID file found. Is the script running?"
    return 1 # Indicate failure
  fi

  PID=$(cat "$PID_FILE")

  if ps -p "$PID" > /dev/null; then
    echo "Stopping process with PID $PID..."
    kill "$PID"
    rm "$PID_FILE"
    echo "Process stopped and PID file removed."
    return 0 # Indicate success
  else
    echo "Process with PID $PID not found. Removing PID file."
    rm "$PID_FILE"
    return 1 # Indicate failure
  fi
}

# Main Logic

stop_script()

# Navigate to the repository directory
cd Desktop/SnakeServerBot/WorldSerpentBot # Need to update this

# Check if there are any local changes
if ! git diff --quiet; then
  echo "There are local changes. Please commit or stash them before pulling."
  exit 1
fi

# Pull the latest changes from the remote repository
git pull origin main

# Check if the pull was successful
if [ $? -eq 0 ]; then
  echo "Successfully pulled the latest changes."
else
  echo "Failed to pull the latest changes."
  exit 1
fi

start_script()

exit 0