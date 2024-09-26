import logging

def log_payment_action(payment_id, action):
    logging.info(f"Payment {payment_id} - Action: {action}")
