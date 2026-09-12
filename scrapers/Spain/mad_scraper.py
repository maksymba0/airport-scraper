from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timezone
from flight import Flight

class MAD_Scraper(BaseScraper):

    airportName_ = "Madrid-Barajas Airport"
    airportCode_ = "MAD"

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
 
        
        data = self.makeRequestHTML("https://www.aeropuertomadrid-barajas.com/eng/madrid-airport-flight-departures.htm", headers=headers)  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser")

        flightList = data_.find("div",class_="flightList")

        records = flightList.find_all("div",class_="flightListRecord")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in records:
  
            tdate = record.find("div", class_="flightListOtherAirport").span.text # "18:00"
 

            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
           
            flight_.date = date 
            flightListFlightIDs = record.find("div", class_="flightListFlightIDs")
            flightListOtherAirport = record.find("div", class_="flightListOtherAirport")
            flightListTimeStatus = record.find("div", class_="flightListTimeStatus")
            flightListTerminal = record.find("div", class_="flightListTerminal")

            timedata = flightListOtherAirport.text.split('-') if flightListOtherAirport else ""
            flight_.destination = timedata[1] if timedata else ""

            flight_.time = timedata[0] if timedata else ""

            flight_.flightNum = flightListFlightIDs.find('a',class_="flightListFlightIDLink").text or  ' '
    
            name = flight_.findAirline()
            flight_.carrier = flightListFlightIDs.find('a',class_="flightListFlightIDAirline").text if name == '-' else name 

            flightListStatus = flightListTimeStatus.find('div',class_="flightListStatus")

            if flightListStatus:
   
                flight_.status = flightListStatus.text or ' '
            else:
                flightListStatus = flightListTimeStatus.find('div').text   

            flight_.gate = flightListTerminal.text or ' ' 
            flight_.type = 'departure'
            flight_.country = 'ES'
            flight_.airport = 'MAD'

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):
 
        print("downloading")
 
        
        data = self.makeRequestHTML("https://www.aeropuertomadrid-barajas.com/eng/madrid-airport-flight-arrivals.htm")  #(url=None, headers=None, method=None):
        
        data_ = bs(data.text,"html.parser")
        
        flightList = data_.find("div",class_="flightList")

        records = flightList.find_all("div",class_="flightListRecord")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for record in records:

            tdate = record.find("div", class_="flightListOtherAirport").span.text # "18:00" 
            flight_ = Flight()

            flight_.time = tdate
            
            date = datetime.today().strftime('%d/%m/%Y') or ' '
            
            flight_.date = date 
            flightListFlightIDs = record.find("div", class_="flightListFlightIDs")
            flightListOtherAirport = record.find("div", class_="flightListOtherAirport")
            flightListTimeStatus = record.find("div", class_="flightListTimeStatus")
            flightListTerminal = record.find("div", class_="flightListTerminal")

            timedata = flightListOtherAirport.text.split() if flightListOtherAirport else ""
            flight_.origin = timedata[2] if timedata else ""

            flight_.time = timedata[0] if timedata else ""

            flight_.flightNum = flightListFlightIDs.find('a',class_="flightListFlightIDLink").text or  ' '
          
            name = flight_.findAirline()
            flight_.carrier = flightListFlightIDs.find('a',class_="flightListFlightIDAirline").text if name == '-' else name 
            flightListStatus = flightListTimeStatus.find('div',class_="flightListStatus")

            if flightListStatus: 
                flight_.status = flightListStatus.text or ' '
            else:
                flightListStatus = flightListTimeStatus.find('div').text   

            flight_.terminal = flightListTerminal.text or ' ' 
            flight_.type = 'arrival'
            flight_.country = 'ES'
            flight_.airport = 'MAD'

            flight = flight_.to_dict()

            flights_info.append(flight) 

            flights_info.append(flight) 
        return flights_info

 