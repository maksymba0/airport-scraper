from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class KTW_Scraper(BaseScraper):

    airportName_ = "Katowice Airport"
    airportCode_ = "KTW"

    def __init__(self, url):
        super().__init__(url)
        print(f"{self.airportCode_} |  {self.airportName_} scraper - init")
        #super().printUrl()

    def makeRequestHTML(self,url=None):
  
        if url is None:
            url = self.url_

        result = super().makeRequestHTML(url) 

        return result 


    def getDepartures(self):

        dateToday = datetime.today().strftime("%Y-%m-%d")
        data = self.makeRequestHTML(f"https://www.katowice-airport.com/pl/api/flight-board/list?direction=1&date={dateToday}&time_from=00:00&time_to=23:59") 

        _data = data
 

        data_ = JSON.loads(_data.text)
           
        flights_info = []
        
        dateNow = datetime.today().strftime("%d/%m/%Y")

        for key in data_['data']: 


            time = key['scheduled_time'] or ''

            flight_ = Flight()
            
            time = key['scheduled_time'] or ''

            flight_.date = dateNow
            flight_.time = time
            flight_.destination = key['airport'] or ' '
            flight_.flightNum = key['flight_number'] or ' '
            flight_.carrier = key['airline_name'] or ' '
            flight_.gate = key['boarding_gate'] or ' '
            flight_.status = key['status'] or ' '


            flight =  flight_.to_dict()
            flights_info.append(flight) 
        return flights_info  

    def getArrivals(self):

        data = ""
        print("downloading") 
        dateToday = datetime.today().strftime("%Y-%m-%d")
        data = self.makeRequestHTML(f"https://www.katowice-airport.com/pl/api/flight-board/list?direction=2&date={dateToday}&time_from=00:00&time_to=23:59")  

        _data = data.text
 

        data_ = JSON.loads(_data)
         

        print(f"Found {len(data_)} elements")

        flights_info = []
        dateNow = datetime.today().strftime("%d/%m/%Y")
        for key in data_['data']: 


            flight_ = Flight()
            
            time = key['scheduled_time'] or ''

            flight_.date = dateNow
            flight_.time = time
            flight_.origin = key['airport'] or ' '
            flight_.flightNum = key['flight_number'] or ' '
            flight_.carrier = key['airline_name'] or ' '
            flight_.terminal = key['boarding_gate'] or ' '
            flight_.status = key['status'] or ' '


            flight =  flight_.to_dict()

            flights_info.append(flight) 
        return flights_info  