from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class LCJ_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Łódź im. Władysława Reymonta Sp. z o.o."
    airportCode_ = "LCJ"

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

        data = self.makeRequestHTML() 

        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("tbody",class_="timetableDepartures")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("td")
                       
            time = tds[0].get_text().split() or ''
            flight = Flight()
             
            flight.time = time[2] #08.08.2026 - 08:25
            flight.date = datetime.strptime(time[0],"%d.%m.%Y").strftime("%d/%m/%Y")
            flight.destination = tds[1].get_text() or ' '
            flight.flightNum = tds[2].get_text() or ' '
            flight.status = tds[3].get_text() or ' '
            carriertext = flight.flightNum

            flight.carrier = ""
            if "RR" in carriertext:
                flight.carrier = "RYANAIR"
            elif "PC" in carriertext:
                flight.carrier = "PEGASUS AIRLINES"
            elif "ENT" in carriertext:
                flight.carrier = "ENTER AIR"
            elif "FR" in carriertext:
                flight.carrier ="RYANAIR"
            elif "KL" in carriertext:
                flight.carrier = "Royal Dutch"
            else:
                flight.carrier = carriertext

            flight_ = flight.to_dict()
            flights_info.append(flight_) 
        return flights_info   

    def getArrivals(self):

        data = ""
        print("downloading")
        data = self.makeRequestHTML()  

        _data = data.text
 

        data_ = bs(_data,"html.parser")

        tbody = data_.find("tbody",class_="timetableArrivals")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("td")
            
            time = tds[0].get_text().split() or ''

            flight = Flight()

            flight.time = time[2] #08.08.2026 - 08:25
            flight.date = datetime.strptime(time[0],"%d.%m.%Y").strftime("%d/%m/%Y")
            flight.origin = tds[1].get_text() or ' '
            flight.flightNum = tds[2].get_text() or ' '
            flight.status = tds[3].get_text() or ' '
            carriertext = flight.flightNum
            flight.carrier = ""
            if "RR" in carriertext:
                flight.carrier = "RYANAIR"
            elif "PC" in carriertext:
                flight.carrier = "PEGASUS AIRLINES"
            elif "ENT" in carriertext:
                flight.carrier = "ENTER AIR"
            elif "FR" in carriertext:
                flight.carrier ="RYANAIR"
            elif "KL" in carriertext:
                flight.carrier = "Royal Dutch"
            else:
                flight.carrier = carriertext

            flight_ = flight.to_dict()

            flights_info.append(flight_) 
        return flights_info  