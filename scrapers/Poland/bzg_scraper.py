from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields
import cloudscraper as CloudScrapper

class BZG_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Bydgoszcz SA"
    airportCode_ = "BZG"

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
    
        data = self.makeRequestHTML("https://plb.pl/wp-admin/admin-ajax.php?action=get_flights_departures") 
         
         
        print("downloading")
        scrapper = CloudScrapper.create_scraper(browser={
                            'browser':'chrome',
                            'platform':'windows',
                            'desktop':True
                        })
        data = scrapper.get(self.url_) 

        _data = data.text

        data_ = JSON.loads(_data)
            

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in data_: 


            time = key['scheduledTime']

            flight_ = Flight()
            
            flight_.time = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%H:%M") or ""
            flight_.origin = key['airportNameEn'] or ' '
            flight_.flightNum = key['flightNumber'] or ' '
            flight_.date = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%d/%m/%Y") or ""
            flight_.carrier = key['airlineName'] or ' '
            flight_.gate = key['gateNumbers'] or ' '
            flight_.status = key['statusEn'] or ' '
            flight = flight_.to_dict()
            flights_info.append(flight) 
            
        return flights_info  
    
    def getArrivals(self):

        print("downloading")

        scrapper = CloudScrapper.create_scraper()
        data = scrapper.get(self.url_)  

        _data = data.text
        print(_data)
        data_ = JSON.loads(_data)
         

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in data_: 


            time = key['scheduledTime']
            flight_ = Flight()

            flight_.time = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%H:%M") or ""
            flight_.origin = key['airportNameEn'] or ' '
            flight_.flightNum = key['flightNumber'] or ' '
            flight_.carrier = key['airlineName'] or ' '
            flight_.date = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%d/%m/%Y") or ""
            flight_.gate = key['gateNumbers'] or ' '
            flight_.status = key['statusEn'] or ' '
            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info  