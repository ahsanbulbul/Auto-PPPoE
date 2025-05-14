#!/bin/bash

# APP_LOCATION="/opt/Auto-PPPoE"
APP_LOCATION="/distros/codeblox/Codes/Projects/Auto-PPPoE"
# Log file path
LOG_FILE="$APP_LOCATION/pppoe_automation.log"

# Add timestamp for start of execution
echo "$(date '+%Y-%m-%d %H:%M:%S') [Start]" >> "$LOG_FILE"
echo "======================================================" >> "$LOG_FILE"

# Change to project directory
cd "$APP_LOCATION"

# Activate the virtual environment
source ~/.venv/bin/activate

# Run the automation script and capture all output
python "$APP_LOCATION/PPPoE_Automation.py" "$@" >> "$LOG_FILE" 2>&1

# Add timestamp for end of execution
echo "======================================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') [Stop]" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Deactivate the virtual environment
deactivate