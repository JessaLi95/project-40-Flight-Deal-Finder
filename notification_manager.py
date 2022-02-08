from twilio.rest import Client
from decouple import config
import smtplib


class NotificationManager:
    def __init__(self):
        self.client = Client(config('ACCOUNT_ID'), config('AUTH_TOKEN'))
        self.my_email = config('MY_EMAIL')
        self.my_password = config('MY_EMAIL_PASSWORD')

    def send_sms(self, content):
        message = self.client.messages.create(
            body=content,
            from_="+16076009148",
            to="+447536128991"
        )
        print(message.status)

    def send_email(self, contact_list, message, booking_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_password)
            for contact in contact_list:
                email = contact['email']
                connection.sendmail(from_addr=self.my_email,
                                    to_addrs=email,
                                    msg=f"Subject: New Low Price Flight!\n\n{message}\nBook your flight now: {booking_link}".encode('utf-8'))
