import schedule
import time
from datetime import datetime
from flask import Flask, request
import subprocess
import logging
import yaml
import os

app = Flask(__name__)

# Load configuration
with open('config/general.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Set up logging
logging.basicConfig(filename=config['log_file'], level=logging.INFO)

# Global variable to store the latest delivery time
latest_delivery_time = None

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_delivery_time
    latest_delivery_time = datetime.now().isoformat()
    logging.info(f"Webhook received at {latest_delivery_time}")
    return "Webhook received", 200

def log_rss_delivery():
    global latest_delivery_time
    if latest_delivery_time:
        # Call the bash script to log the delivery time
        subprocess.run(['bash', 'scripts/log_rss_delivery.sh', latest_delivery_time])
        logging.info(f"Logged RSS feed delivery time: {latest_delivery_time}")
        latest_delivery_time = None
    else:
        logging.info("No RSS feed delivery since last check")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Schedule the logging task to run every day at noon
    schedule.every().day.at("12:00").do(log_rss_delivery)

    # Run the Flask app in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()

    # Run the scheduler
    run_schedule()

# Usage instructions
"""
To use this RSS feed logger:
1. Ensure the configuration in config/general.yaml is correct, especially the 'log_file' path.
2. Run this script: python scripts/rss_feed_logger.py
3. The script will start a Flask server listening for webhooks on port 5000.
4. Configure your RSS feed service to send a POST request to http://your-server-ip:5000/webhook when a new feed is delivered.
5. The script will log the delivery times and run the log_rss_delivery.sh script daily at noon.

To update:
1. Modify the config/general.yaml file to change logging or other settings.
2. If you need to change the scheduling, modify the schedule.every().day.at("12:00") line in this script.
3. To add new functionality, you can extend the webhook function or add new routes as needed.
"""
