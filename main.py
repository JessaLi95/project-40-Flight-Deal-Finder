from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

flightSearch = FlightSearch()
dataManager = DataManager()
sheet_data = dataManager.flights_get()
notificationManager = NotificationManager()
contact_list = dataManager.users_get()


for i in range(len(sheet_data)):
    if len(sheet_data[i]['iataCode']) == 0:
        city_code = flightSearch.get_iataCode(sheet_data[i]['city'])
        dataManager.flights_put(i + 2, city_code)
    else:
        flight_detail = flightSearch.search_flight(sheet_data[i]['iataCode'], sheet_data[i]['city'])
        if flight_detail is None:
            continue
        elif flight_detail['price'] <= sheet_data[i]['lowestPrice']:
            price = flight_detail["price"]
            cityCodeFrom = flight_detail['cityCodeFrom']
            cityTo = sheet_data[i]['city']
            cityCodeTo = flight_detail['cityCodeTo']
            outDate = flight_detail['outbound_date']
            inDate = flight_detail['inbound_date']
            try:
                via_city = flight_detail['via_city']
                message = f"Price price alert! Only £{price} to fly from London-{cityCodeFrom} to {cityTo}-{cityCodeTo}, from {outDate} to {inDate}.\nFlight has 1 stop over, via {via_city}"
            except KeyError:
                message = f"Price price alert! Only £{price} to fly from London-{cityCodeFrom} to {cityTo}-{cityCodeTo}, from {outDate} to {inDate}. "
            finally:
                booking_link = f"https://www.kayak.co.uk/flights/{cityCodeFrom}-{cityCodeTo}/{outDate}/{inDate}?sort=bestflight_a"
                notificationManager.send_email(contact_list, message, booking_link)
                print(message)

