import requests
import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()
class DataManager:
    def __init__(self):
    
        self.PRICES_ENDPOINT = os.getenv("API_ENDPOINT")
        self.USER_NAME= os.getenv("USER_NAME")
        self.PASSWORD= os.getenv("PASSWORD")
        self.auth = HTTPBasicAuth(self.USER_NAME, self.PASSWORD)
        self.get_destination={}
    def get_destination_data(self):
        response = requests.get(url=self.PRICES_ENDPOINT, auth=self.auth)
        response.raise_for_status()
        data = response.json()
        self.get_destination = data["prices"]
        return self.get_destination
    def update_destination_codes(self):
        for city in self.get_destination:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
            )
            
    


    