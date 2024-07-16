from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_data import FlightData
from notification_manager import NotificationManager
notification_manager = NotificationManager()
flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
user_data = data_manager.get_customer_emails()
user_list= [user['Email'] for user in user_data]
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
        if cheapest_flight.stop_over == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}"
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."
        print(f"Check your email. Lower price flight found to {row['city']}!")
        notification_manager.send_emails(user_list, message)
        notification_manager.send_sms(message)
