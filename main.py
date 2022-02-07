from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

flightSearch = FlightSearch()
dataManager = DataManager()
sheet_data = dataManager.app_get()
notificationManager = NotificationManager()

for i in range(len(sheet_data)):
    if len(sheet_data[i]['iataCode']) == 0:
        city_code = flightSearch.get_iataCode(sheet_data[i]['city'])
        dataManager.app_put(i+2, city_code)
    else:
        flight_detail = flightSearch.search_flight(sheet_data[i]['iataCode'], sheet_data[i]['city'])
        if flight_detail is not None and flight_detail['price'] <= sheet_data[i]['lowestPrice']:
            price = flight_detail["price"]
            cityCodeFrom = flight_detail['cityCodeFrom']
            cityTo = sheet_data[i]['city']
            cityCodeTo = flight_detail['cityCodeTo']
            outDate = flight_detail['outbound_date']
            inDate = flight_detail['inbound_date']
            notificationManager.sms_message(price, cityCodeFrom, cityTo, cityCodeTo, outDate, inDate)



