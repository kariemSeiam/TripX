import logging

def log_withdrawal_action(withdrawal_id, action):
    logging.info(f"Withdrawal {withdrawal_id} - Action: {action}")
