import requests
import logging
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(dir_path, 'events.log'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

def fetch_github_events():
    r = requests.get('https://api.github.com/users/python-engineer/events')
    events = r.json()
    if events and len(events):
        last_event = events[0]
        logger.info(last_event)
    else:
        logger.error('Could not get last event')
    

if __name__ == '__main__':
    fetch_github_events()
    