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
            print(f"No direct flight to {ticket_parameters['fly_to']}")
            ticket_parameters["max_stopovers"] = 1
            try:
                flight_1_stop = requests.get(search_url, headers=HEADER, params=ticket_parameters).json()["data"][0]
            except IndexError:
                print(f"No flight to {ticket_parameters['fly_to']} with 1 stopover.")
                return None
            else:
                print(f"Stop over {flight_1_stop['route'][0]['cityTo']}: £{flight_1_stop['price']}")
                return {
                    "cityCodeFrom": flight_1_stop['flyFrom'],
                    "cityCodeTo": flight_1_stop['flyTo'],
                    "price": flight_1_stop['price'],
                    "outbound_date": flight_1_stop['route'][0]['local_departure'].split('T')[0],
                    "inbound_date": flight_1_stop['route'][1]['local_departure'].split('T')[0],
                    "stop_over": 1,
                    "via_city": flight_1_stop["route"][0]["cityTo"]
                }
        else:
            print(f"{city}: £{ticket_response['price']}")
            return {
                "cityCodeFrom": ticket_response['flyFrom'],
                "cityCodeTo": ticket_response['flyTo'],
                "price": ticket_response['price'],
                "outbound_date": ticket_response['route'][0]['local_departure'].split('T')[0],
                "inbound_date": ticket_response['route'][1]['local_departure'].split('T')[0],
            }
