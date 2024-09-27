import logging
import os
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

class SMSServiceConfig:
    SMS_API_KEY = os.environ.get('SMS_API_KEY', 'default_api_key')
    SMS_API_URL = os.environ.get('SMS_API_URL', 'https://api.example.com/send_sms')
    RETRY_COUNT = 3

class SMSService:
    def __init__(self):
        self.logger = logging.getLogger('sms_service')
        handler = logging.FileHandler('logs/sms_service.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def send_sms(self, phone_number, message):
        for attempt in range(SMSServiceConfig.RETRY_COUNT):
            try:
                response = requests.post(
                    SMSServiceConfig.SMS_API_URL,
                    data={'key': SMSServiceConfig.SMS_API_KEY, 'to': phone_number, 'message': message}
                )
                response.raise_for_status()
                self.logger.info(f"SMS sent to {phone_number}: {message}")
                return True
            except (HTTPError, ConnectionError, Timeout) as e:
                self.logger.warning(f"Attempt {attempt + 1}: Failed to send SMS to {phone_number}: {str(e)}")
            except RequestException as e:
                self.logger.error(f"RequestException: Failed to send SMS to {phone_number}: {str(e)}")
                break
        return False
