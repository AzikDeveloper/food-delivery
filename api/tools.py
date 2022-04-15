from twilio.rest import Client
from random import randint
from django.conf import settings


class SMS:
    def __init__(self, to_phone_number):
        self.to_phone_number = to_phone_number
        self.code = randint(100000, 999999)

    def generate_code(self):
        self.code = randint(100000, 999999)

    def send_sms(self):
        if settings.TWILIO_SEND_SMS:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                to=self.to_phone_number,
                from_=settings.TWILIO_FROM_NUMBER,
                body=f'Food Delivery {self.code}'
            )
