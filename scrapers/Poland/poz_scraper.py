from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight
from cloudscraper import CloudScraper

class POZ_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Poznań-Ławica Sp. z o.o."
    airportCode_ = "POZ"

    def __init__(self, url):
        super().__init__(url)
        print(f"{self.airportCode_} |  {self.airportName_} scraper - init")
        #super().printUrl()

    def makeRequestHTML(self,url=None):
  
        if url is None:
            url = self.url_

        header_ = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
        }
        #result = super().makeRequestHTML(url, method=None, headers=header_) 
        scraper = CloudScraper.create_scraper()
        result = scraper.get(self.url_) 
        # requests.get(self.url_)

        return result 


    def getDepartures(self):
    
        data = self.makeRequestHTML("https://poznanairport.pl/wp-json/api/v1/board/?page=1&phrase=&type=departures&day=0&timeFrom=00:00&timeTo=23:59&count=10&lang=pl") 
                                    
        _data = data
 

        data_ = JSON.loads(_data.text)
           
        flights_info = []
        for key in data_['data']: 


            time = key['date']['label'] or ''
            flight_ = Flight()

            flight_.time = time
            flight_.date = datetime.strptime(key['date_only'],"%Y-%m-%d").strftime("%d/%m/%Y")
            flight_.destination = key['airport']['label'] or ' '
            flight_.flightNum = key['flight_id'] or ' '
            flight_.carrier = key['airline']['label'] or ' '
            flight_.gate = key['gate']['value'] or ' '
            flight_.status = key['status']['value'] or ' '
            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info  

    def getArrivals(self):
 
        print("downloading")
        data = self.makeRequestHTML()  
 
        data_ = data.json()
          
        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in data_['data']:  
            
            time = key['date']['label'] or ''

            flight_ = Flight()
            
            flight_.time = time
            flight_.date = datetime.strptime(key['date_only'],"%Y-%m-%d").strftime("%d/%m/%Y")
            flight_.origin = key['airport']['label'] or ' '
            flight_.flightNum = key['flight_id'] or ' '
            flight_.carrier = key['airline']['label'] or ' '
            flight_.gate = key['gate']['value'] or ' '
            flight_.status = key['status']['value'] or ' '
            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info  