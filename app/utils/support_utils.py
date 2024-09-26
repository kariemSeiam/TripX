import logging

def log_support_action(ticket_id, action, message_id=None):
    logging.info(f"Support Ticket {ticket_id} - Action: {action} - Message ID: {message_id}")
