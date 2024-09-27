import logging

def log_payment_action(payment_id, action):
    """Log actions performed on payments."""
    logging.info(f"Payment {payment_id} - Action: {action}")
