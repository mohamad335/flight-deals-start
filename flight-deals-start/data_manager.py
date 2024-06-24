import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()
SHEETY_ENDPOINT="https://api.sheety.co/1229a7668b922a6cc01b2817f04a99c9/copyOfFlightDeals/prices"
class DataManager:
    def __init__(self):
        self._USERNAME=os.environ["USERNAME"]
        self._PASSWORD=os.environ["PASSWORD"]
        self.auth=HTTPBasicAuth(username=self._USERNAME, password=self._PASSWORD)
        self.Get_Data={}
    def get_data(self):
        response=requests.get(url=SHEETY_ENDPOINT,headers=self.header)
        data=response.json()
        self.Get_Data=data["prices"]
        return self.Get_Data
    def update_iata(self):
        for city in self.Get_Data:
            new_data={
                "price":{
                    "iataCode":city["iataCode"]
                }
            }
            response=requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data, headers=self.header)
            print(response.text)
        

    