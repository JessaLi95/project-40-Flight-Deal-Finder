import requests
from decouple import config
from datetime import datetime, timedelta
api_key = config('TEQUILA_KEY')

HEADER = {
            "apikey": api_key
        }


class FlightSearch:
    def get_iataCode(self, city):
        get_url = "https://tequila-api.kiwi.com/locations/query"
        code_parameters = {
            "term": city
        }
        code_response = requests.get(url=get_url, headers=HEADER, params=code_parameters).json()
        return code_response["locations"][0]["code"]

    def search_flight(self, iataCode, city):
        search_url = "https://tequila-api.kiwi.com/v2/search"
        ticket_parameters = {
            "fly_from": "LON",
            "fly_to": iataCode,
            "date_from": (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y"),
            "date_to": (datetime.today() + timedelta(days=181)).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "GBP",
            "one_for_city": 1,
            "max_stopovers": 0
            }
        try:
            ticket_response = requests.get(search_url, headers=HEADER, params=ticket_parameters).json()["data"][0]
        except IndexError:
            print(f"No flight found for {city}.")
            return None
        else:
            print(f"{city}: £{ticket_response['price']}")
            return {
                "cityCodeFrom": ticket_response['flyFrom'],
                "cityCodeTo": ticket_response['flyTo'],
                "price": ticket_response['price'],
                "outbound_date": ticket_response['route'][0]['local_departure'].split('T')[0],
                "inbound_date": ticket_response['route'][1]['local_departure'].split('T')[0]
            }
