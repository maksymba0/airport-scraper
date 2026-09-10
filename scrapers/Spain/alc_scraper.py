from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timezone
from flight import Flight

class ALC_Scraper(BaseScraper):

    airportName_ = "Alicante–Elche Miguel Hernández Airport"
    airportCode_ = "ALC"

    def __init__(self, url):
            super().__init__(url)
            print(f"{self.airportCode_} |  {self.airportName_} scraper - init")

    def makeRequestHTML(self,url=None, headers=None, method=None, json=None):

        header_ = headers or None
        method_ = method or None
        payload_ = json or None
        if url is None:
            url = self.url_
 
        result = super().makeRequestHTML(url, headers=header_,method=method_,json=payload_)
            
        return result 


    def getDepartures(self):

        data = ""
        print("downloading")

        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/json"
            }
 
        
        data = self.makeRequestHTML()  #(url=None, headers=None, method=None):
        
        data_ = data.json() 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for flight in data_:

            tdate = datetime.fromtimestamp(flight["scheduledTime"],timezone.utc);
            time = tdate or ''

            flight_ = Flight()

            flight_.time = time.strftime("%H:%M")
            
            date = time.strftime("%d/%m/%Y") or ' '
           
            flight_.date = date
            flight_.destination = flight["cityInitial"] or ' '
            flight_.flightNum = flight["numFlight"] or ' '
            flight_.carrier = flight["nameCompany"] or ' '
            flight_.status = flight["status"] or ' '
            flight_.gate = flight["gate"] or ' '
            flight_.country = 'ES'
            flight_.airport = 'ALC'

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):
        
        data = ""
        print("downloading")

        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/json"
            }
    
        
        data = self.makeRequestHTML("https://alicanteairport.es/arrivals.json")  #(url=None, headers=None, method=None):
        
        data_ = data.json() 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for flight in data_:

            tdate = datetime.fromtimestamp(flight["scheduledTime"],timezone.utc);
            time = tdate or ''

            flight_ = Flight()

            flight_.time = time.strftime("%H:%M")
            
            date = time.strftime("%d/%m/%Y") or ' '
            
            flight_.date = date
            flight_.destination = flight["cityInitial"] or ' '
            flight_.flightNum = flight["numFlight"] or ' '
            flight_.carrier = flight["nameCompany"] or ' '
            flight_.status = flight["status"] or ' '
            flight_.gate = flight["baggage_belt"] or ' '
            flight_.country = 'ES'
            flight_.airport = 'ALC'

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

 