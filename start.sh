#!/bin/bash

API_DIR="./my_app/api"

# Activate virtual environment
source "${API_DIR}/venv/bin/activate"

# Define custom commands
function start_server() {
    python "${API_DIR}/main.py"
}

function start_client() {
    cd my_app/app && npm run start
}

# Execute custom command based on argument
case "$1" in
    start_server)
        start_server
        ;;
    start_client)
        start_client
        ;;
    *)
        echo "Usage: $0 {start_server|start_client}"
        exit 1
esac



# execute command like this: ./start.sh start_server ./start.sh start_client