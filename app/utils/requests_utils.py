import logging

def log_request_action(request_id, action):
    logging.info(f"Request {request_id} - Action: {action}")
