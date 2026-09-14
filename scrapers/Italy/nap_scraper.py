from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timezone
from flight import Flight

class NAP_Scraper(BaseScraper):

    airportName_ = "Naples Airport"
    airportCode_ = "NAP"

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
        
        data = self.makeRequestHTML("https://www.aeroportodinapoli.it/en/departures", headers=headers)  #(url=None, headers=None, method=None):

        data_ = bs(data.text,"html.parser") 

        departures = data_.find_all('div',class_='single-flight row')
 
        rows = departures
        
        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows:

            elements = record
    
            raw_text = record.select_one('.timetables .expected')
            tdate = raw_text.text.strip() or " "

            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date
             
            flight_.destination = record.select_one('.flight-info .col info')



            flight_.flightNum = elements['flights'][0]['number']

            flight_.carrier = flight_.flightNum if (airline := flight_.findAirline()) == '-' else airline

            flightListStatus = elements['status']['description']

            flight_.status = flightListStatus or ' '

            flight_.gate = '  ' 
            flight_.type = 'departure'
            flight_.country = 'IT'
            flight_.airport = self.airportCode_

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):
 
        print("downloading") 
        
        data = self.makeRequestHTML("https://www.milanbergamoairport.it/en/real-time-flights/")  #(url=None, headers=None, method=None):
                
        data_ = bs(data.text,"html.parser")

        arrivals = data_.find('div',id="arr-table")
        rows = arrivals.find('tbody').find_all('tr') 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows:

            elements = record.find_all('td')
 
            raw_text = elements[3].text.strip().replace('"', '')
            tdate = raw_text.split()[1] if raw_text else " "
            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date 
                 
            flight_.origin = next(elements[2].stripped_strings, " ").replace('"', '')
            flight_.flightNum = elements[1].text.strip().replace('"', '') or  ' '
    

            flight_.carrier = flight_.flightNum if (airline := flight_.findAirline()) == '-' else airline

            flightListStatus = elements[5].text.strip().replace('"', '') or ' '

            flight_.status = flightListStatus or ' '

            flight_.gate = ' ' 
            flight_.type = 'arrival'
            flight_.country = 'IT'
            flight_.airport = self.airportCode_

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

 