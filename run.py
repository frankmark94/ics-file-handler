#!/usr/bin/env python3
"""
ICS File Handler - Runner Script
This script runs the ICS File Handler web application.
"""

from app import app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ics_handler')

if __name__ == '__main__':
    logger.info("==== Starting ICS File Handler ====")
    logger.info("Open your browser and navigate to one of these URLs:")
    logger.info("http://localhost:8080")
    logger.info("http://127.0.0.1:8080")
    logger.info("http://10.0.0.144:8080")  # Using your specific IP address
    
    # Run the Flask application
    try:
        app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
    except Exception as e:
        logger.error(f"Error starting Flask: {e}")
        print(f"ERROR: {e}") 