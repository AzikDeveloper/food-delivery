from twilio.rest import Client
from random import randint


class SMS:
    def __init__(self, to_phone_number):
        self.to_phone_number = to_phone_number
        self.code = randint(100000, 999999)

    def generate_code(self):
        self.code = randint(100000, 999999)

    def send_sms(self):
        if send_sms:
            client = Client(account_sid, auth_token)
            client.messages.create(
                to=self.to_phone_number,
                from_=from_phone_number,
                body=f'Food Delivery {self.code}'
            )
