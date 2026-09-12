from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timezone
from flight import Flight
from utils import get_airline_name
class LPA_Scraper(BaseScraper):

    airportName_ = "La Gran Canaria Airport"
    airportCode_ = "LPA"

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
 
        
        data = self.makeRequestHTML("https://www.avionio.com/widget/en/lpa/departures", headers=headers)  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser") 

        rows = data_.select('.tt-row') 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows:

            elements = record.find_all('td')

            
            tdate = elements[0].text.strip().replace('"', '')
            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
           
            flight_.date = date 
               
            flight_.destination = elements[3].text.strip().replace('"', '') or " " 

            flight_.flightNum = elements[4].text.strip().replace('"', '') or  ' '
    
         
            airlineName = flight_.findAirline()
            flight_.carrier = elements[5].text.strip().replace('"', '') if airlineName == '-' else airlineName
            flightListStatus = elements[6].text.strip().replace('"', '') or ' '

            flight_.status = flightListStatus or ' '

            flight_.gate = '' 
            flight_.type = 'departure'
            flight_.country = 'ES'
            flight_.airport = 'LPA' 

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):
 
        print("downloading") 
        
        data = self.makeRequestHTML("https://www.avionio.com/widget/en/lpa/arrivals")  #(url=None, headers=None, method=None):
                
        data_ = bs(data.text,"html.parser") 

        rows = data_.select('.tt-row') 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows:

            elements = record.find_all('td')
 
            tdate = elements[0].text.strip().replace('"', '')
            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date 
                
            flight_.origin = elements[3].text.strip().replace('"', '') or " " 

            flight_.flightNum = elements[4].text.strip().replace('"', '') or  ' '
    

            airlineName = flight_.findAirline() 
            flight_.carrier = elements[5].text.strip().replace('"', '') if airlineName == '-' else airlineName
            flightListStatus = elements[6].text.strip().replace('"', '') or ' '

            flight_.status = flightListStatus or ' '

            flight_.gate = '' 
            flight_.type = 'arrival'
            flight_.country = 'ES'
            flight_.airport = 'LPA'

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

 