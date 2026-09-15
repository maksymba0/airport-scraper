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
        
        data = self.makeRequestHTML("https://www.avionio.com/widget/en/nap/departures", headers=headers)  #(url=None, headers=None, method=None):

        data_ = bs(data.text,"html.parser") 
 
        departures = data_.find('table',class_='tt').find('tbody')

        target_rows = departures.select('tr.tt-row.estimated')

        
        print(f"Found {len(target_rows)} elements")

        flights_info = []
        for record in target_rows: 
 
            elements = record.find_all('td') 

            raw_text = elements[0]
            tdate = raw_text.text.strip() or " "

            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date
             
            flight_.destination = elements[3].text.strip() or ' '



            flight_.flightNum = elements[4].find('a').text.strip() or ' '

            flight_.carrier = flight_.flightNum if (airline := flight_.findAirline()) == '-' else airline

            flightListStatus = elements[6].text.strip() or ' '

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
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
        } 
        data = self.makeRequestHTML("https://www.avionio.com/widget/en/nap/arrivals", headers=headers)  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser") 
    
        departures = data_.find('table',class_='tt').find('tbody')

        target_rows = departures.select('tr.tt-row.estimated')

        
        print(f"Found {len(target_rows)} elements")

        flights_info = []
        for record in target_rows: 
    
            elements = record.find_all('td') 

            raw_text = elements[0]
            tdate = raw_text.text.strip() or " "

            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date
                
            flight_.origin = elements[3].text.strip() or ' '



            flight_.flightNum = elements[4].find('a').text.strip() or ' '

            flight_.carrier = flight_.flightNum if (airline := flight_.findAirline()) == '-' else airline

            flightListStatus = elements[6].text.strip() or ' '

            flight_.status = flightListStatus or ' '

            flight_.gate = ' ' 
            flight_.type = 'arrival'
            flight_.country = 'IT'
            flight_.airport = self.airportCode_

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

 