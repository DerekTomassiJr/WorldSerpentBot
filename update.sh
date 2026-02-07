# Function to stop the Python script
stop_script() {
  PROCESS_NAME = "world_serpent.py"

  PID=$(pgrep -f "$PROCESS_NAME")
  
  if [ -z "$PID" ]; then
    echo "No process found for $PROCESS_NAME."
  else
    echo "Found process with PID: $PID"
    kill "$PID"
    echo "Process $PID - $PROCESS_NAME has been stopped."
}

start_script() {
  cd Desktop/SnakeServerBot/WorldSerpentBot
  
  echo "Starting world_serpent.py"
  Python world_serpent.py
}

# Main Logic
stop_script()

# Navigate to the repository directory
cd Desktop/SnakeServerBot/WorldSerpentBot # Need to update this

# Pull the latest changes from the remote repository
git pull origin main

start_script()

exit 0
