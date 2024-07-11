from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()
class NotificationManager:
    def __init__(self):
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)
    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=os.getenv("MY_PHONE_NUMBER"),
            to=os.getenv("TO")
        )
        print(message.sid)

    
