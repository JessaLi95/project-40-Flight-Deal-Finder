import requests
from decouple import config
url = config('SHEETY')


class DataManager:
    def app_get(self):
        get_url = url
        get_response = requests.get(get_url).json()
        return get_response["prices"]

    def app_put(self, row_id, iata_code):
        put_url = f"{url}/{row_id}"
        put_body = {
            "price": {
                "iataCode": iata_code
            }
        }
        put_response = requests.put(put_url, json=put_body)
        put_response.raise_for_status()
