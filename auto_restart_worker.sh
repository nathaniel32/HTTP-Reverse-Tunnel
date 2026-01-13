#!/bin/bash

PYTHON_CMD="python3"
PYTHON_ARGS="-m"
SCRIPT_PATH="worker.main"
RESTART_DELAY=5

while true
do
    echo "Running $PYTHON_CMD $PYTHON_ARGS $SCRIPT_PATH $@"
    "$PYTHON_CMD" $PYTHON_ARGS "$SCRIPT_PATH" "$@"

    echo "$SCRIPT_PATH crashed. Restarting in $RESTART_DELAY seconds..."
    sleep $RESTART_DELAY
done