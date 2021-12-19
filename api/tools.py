from twilio.rest import Client
from random import randint

account_sid = "ACa1ea63f1a96512f69d5b667950f3a692"
auth_token = "e34b0e652bee60228895a121d0aad9cd"
from_phone_number = "+12182923493"


class SMS:
    def __init__(self, to_phone_number):
        self.to_phone_number = to_phone_number
        self.code = randint(100000, 999999)

    def generate_code(self):
        self.code = randint(100000, 999999)

    def send_sms(self):
        client = Client(account_sid, auth_token)
        client.messages.create(
            to=self.to_phone_number,
            from_=from_phone_number,
            body=f'Food Delivery {self.code}'
        )
