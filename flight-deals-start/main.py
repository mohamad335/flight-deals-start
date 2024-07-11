from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_data import FlightData
from notification_manager import NotificationManager
notification_manager = NotificationManager()
flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        

ORIGEN = "LON"
tomorrow = datetime.now() + timedelta(days=1)
after_sixMonths = tomorrow + timedelta(days=180)
for row in sheet_data:
    flight = flight_search.check_flights(
        ORIGEN,
        row["iataCode"],
        from_time=tomorrow,
        to_time=after_sixMonths,
    )
    cheapest_flight = FlightData.find_cheapest_flight(flight)
    if cheapest_flight.price!="N/A" and cheapest_flight.price < row["lowestPrice"]:
        print(f"Cheapest flight to {row['city']} is {cheapest_flight.price}")
        message = f"Low price alert! Only £{cheapest_flight.price} to fly from {ORIGEN}-{row['iataCode']} to {row['city']} from {cheapest_flight.origin_airport}-{cheapest_flight.destination_airport}, from {cheapest_flight.out_date} to {cheapest_flight.return_date}."
        notification_manager.send_sms(message)


