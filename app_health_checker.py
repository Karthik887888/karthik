import requests
import logging
from datetime import datetime

# Set up logging to log to a file
logging.basicConfig(filename="app_health.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Application URL to be checked
APP_URL = "http://application_url_here.com"  #URL of application

def check_application_health():
    try:
        # Send an HTTP GET request to the application with a timeout of 5 seconds
        response = requests.get(APP_URL, timeout=5)

        # Check if the status code is 200 (OK)
        if response.status_code == 200:
            logging.info(f"Application is healthy. Status Code: {response.status_code}")
            print(f"[{datetime.now()}] Application is healthy. Status Code: {response.status_code}")
        else:
            logging.warning(f"Application might be down. Status Code: {response.status_code}")
            print(f"[{datetime.now()}] Application might be down. Status Code: {response.status_code}")

    except requests.exceptions.Timeout:
        # Handle request timeout
        logging.error("Request timed out.")
        print(f"[{datetime.now()}] Request timed out.")

    except requests.exceptions.ConnectionError:
        # Handle connection errors (e.g., DNS failure, refused connection)
        logging.error("Failed to connect to the application.")
        print(f"[{datetime.now()}] Failed to connect to the application.")

    except requests.exceptions.RequestException as e:
        # Catch other network-related errors
        logging.error(f"Failed to reach application: {e}")
        print(f"[{datetime.now()}] Failed to reach application: {e}")

if __name__ == "__main__":
    check_application_health()
