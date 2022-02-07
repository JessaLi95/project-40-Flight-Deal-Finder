from twilio.rest import Client
from decouple import config
account_id = config('ACCOUNT_ID')
auth_token = config('AUTH_TOKEN')


class NotificationManager:
    def sms_message(self, price, cityCodeFrom, cityTo, cityToCode, outDate, inDate):
        content = f"Price price alert! Only £{price} to fly from London-{cityCodeFrom} to {cityTo}-{cityToCode}, " \
                  f"from {outDate} to {inDate}."
        client = Client(account_id, auth_token)
        message = client.messages.create(
            body=content,
            from_="+16076009148",
            to="+447536128991"
        )
        print(message.status)

