import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
class FlightSearch:
    def __init__(self):
        self._api_key=os.environ["API_KEY"]
        self._api_secret=os.environ["API_SECRET"]
        self._token=self._get_new_token()


        
    def get_code(self, city_name):
        code = "TESTING"
        return code
    def _get_new_token(self):
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id':self._api_key ,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=body)
        data=response.json()
        return data["access_token"]
    def get_iata(self, city):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        params = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=params)
        data = response.json()
        return data["data"][0]["iataCode"]
        try:
            code = data["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport found for {city}.")
            return None
        except KeyError:
            print(f"Invalid response from the API for {city}.")
            return None
        return code

    
    