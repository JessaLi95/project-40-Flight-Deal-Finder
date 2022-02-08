import requests
from decouple import config


class DataManager:
    def __init__(self):
        self.flight_url = config('SHEETY_FLIGHTS')
        self.user_url = config('SHEETY_USERS')

    def flights_get(self):
        get_response = requests.get(self.flight_url).json()
        return get_response["prices"]

    def flights_put(self, row_id, iata_code):
        put_url = f"{self.flight_url}/{row_id}"
        put_body = {
            "price": {
                "iataCode": iata_code
            }
        }
        put_response = requests.put(put_url, json=put_body)
        put_response.raise_for_status()

    def users_get(self):
        user_get_response = requests.get(self.user_url).json()
        return user_get_response['users']



