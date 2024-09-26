import logging

def log_conversation_action(conversation_id, action, message_id=None):
    logging.info(f"Conversation {conversation_id} - Action: {action} - Message ID: {message_id}")
