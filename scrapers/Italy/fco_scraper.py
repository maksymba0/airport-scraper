from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timezone
from flight import Flight

class FCO_Scraper(BaseScraper):

    airportName_ = "Rome-Fiumicino Airport"
    airportCode_ = "FCO"

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
    
        
        data = self.makeRequestHTML("https://www.adr.it/web/aeroporti-di-roma-en/pax-fco-realtime-flight", headers=headers)  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser") 

        departures = data_.find('div',class_="table-responsive").find('tbody')
    
        rows = departures.find_all('tr') 
        
        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows[:-1]:

            elements = record.find_all('td')
    
            raw_text = elements[0].text.strip().replace('"', '')
            tdate = raw_text.split()[2] if raw_text else " "

            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date
            #print(elements[2])
            destination_tag = elements[2].find('h5', class_='blue-title').text
 
            rawtext = " ".join(destination_tag.split())
            flight_.destination = rawtext if destination_tag else ' '

            flight_a = record.select_one('div.flight-code a')
            flight_.flightNum = flight_a.text.strip() if flight_a else ' '

            #print(record.find('div',class_='carrier-logo'))

            carrier_span = record.select_one('.carrier-logo span')
            carrier = carrier_span.text.strip() if carrier_span else ' '


            flight_.carrier = carrier if (airline := flight_.findAirline()) == '-' else airline
 
            flightListStatus = elements[4].find('h5').text.strip().replace('"', '') or ' '

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

        data = self.makeRequestHTML("https://www.adr.it/web/aeroporti-di-roma-en/pax-fco-realtime-flight?p_p_id=3_WAR_realtimeflightsportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_3_WAR_realtimeflightsportlet_redirect=%2Fweb%2Faeroporti-di-roma-en-%2Fpax-fco-fiumicino&_3_WAR_realtimeflightsportlet_tab=arrival&_3_WAR_realtimeflightsportlet_searchType=completeSmall", headers=headers)  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser") 

        departures = data_.find('div',class_="table-responsive").find('tbody')
    
        rows = departures.find_all('tr') 

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in rows[:-1]:

            elements = record.find_all('td')
               
            raw_text = elements[0].text.strip().replace('"', '')
            tdate = raw_text.split()[2] if raw_text else " "

            
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date
            #print(elements[2])
            destination_tag = elements[2].find('h5', class_='blue-title').text

            rawtext = " ".join(destination_tag.split())
            flight_.origin = rawtext if destination_tag else ' '

            flight_a = record.select_one('div.flight-code a')
            flight_.flightNum = flight_a.text.strip() if flight_a else ' '

            #print(record.find('div',class_='carrier-logo'))

            carrier_span = record.select_one('.carrier-logo span')
            carrier = carrier_span.text.strip() if carrier_span else ' '


            flight_.carrier = carrier if (airline := flight_.findAirline()) == '-' else airline

            flightListStatus = elements[4].find('h5').text.strip().replace('"', '') or ' '

            flight_.status = flightListStatus or ' '

            flight_.gate = ' ' 
            flight_.type = 'arrival'
            flight_.country = 'IT'
            flight_.airport = self.airportCode_

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

 