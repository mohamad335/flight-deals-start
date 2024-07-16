import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_API="https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("API_KEY")
        self._secret_api= os.getenv("API_SECRET")
        self.token = self.get_new_token()
    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        sheety_token = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._secret_api
        }
        response = requests.post(
            url=TOKEN_API,
            headers=header,data=sheety_token
        )
        data = response.json()['access_token']
        return data
        
    def get_destination_code(self, city_name):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        query = {
            "keyword":city_name,
            "max":"2",
            "include":"AIRPORTS"
            
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=header,
            params=query
        )
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time,is_direct=True):
        
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate":from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": True if is_direct else False,
            "currencyCode": "GBP",
            "max": "10",
        }
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")

            return None

        return response.json()

    

    
    
    