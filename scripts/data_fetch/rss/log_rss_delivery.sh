#!/bin/bash

LOG_FILE="rss_delivery.log"
MAX_SIZE=1048576  # 1 MB

if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -ge $MAX_SIZE ]; then
    mv "$LOG_FILE" "${LOG_FILE}.$(date +%Y%m%d%H%M%S)"
    echo "Log rotated at $(date)" >> "$LOG_FILE"
fi

# Check if a timestamp was provided
if [ $# -eq 0 ]; then
    echo "No timestamp provided. Usage: $0 <timestamp>"
    exit 1
fi

# Get the timestamp from the argument
timestamp=$1

# Log file path
log_file="/var/log/rss_feed_delivery.log"

# Append the timestamp to the log file
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Feed delivered: $FEED_URL" >> "$LOG_FILE"

# Print confirmation
echo "Logged RSS feed delivery time to $log_file"
