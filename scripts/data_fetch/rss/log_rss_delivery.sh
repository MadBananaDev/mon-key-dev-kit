#!/bin/bash

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
echo "RSS feed delivered at: $timestamp" >> "$log_file"

# Print confirmation
echo "Logged RSS feed delivery time to $log_file"
