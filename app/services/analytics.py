import logging

class Analytics:
    def __init__(self):
        self.logger = logging.getLogger('analytics')
        handler = logging.FileHandler('logs/analytics.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_event(self, event_name, data):
        self.logger.info(f"Event: {event_name}, Data: {data}")
