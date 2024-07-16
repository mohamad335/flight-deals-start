import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.getenv("AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)
        self._email = os.getenv("EMAIL")
        self._password = os.getenv("APP_PASS")
    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=os.getenv("MY_PHONE_NUMBER"),
            to=os.getenv("TO")
        )
        print(message.sid)
    def send_emails(self, message, emails):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self._email, password=self._password)
            for email in emails:
                connection.sendmail(
                    from_addr=self._email,
                    to_addrs=email,
                    msg=f"Subject:Flight Deals\n\n{message}".encode('utf-8')
                )
    
