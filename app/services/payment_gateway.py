import logging

class PaymentGateway:
    def __init__(self):
        self.logger = logging.getLogger('payment_gateway')
        handler = logging.FileHandler('logs/payment_gateway.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def process_payment(self, amount, payment_details):
        # Implement payment processing logic
        self.logger.info(f"Processing payment of {amount} with details {payment_details}")
