from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class LUZ_Scraper(BaseScraper):

    airportName_ = "Port lotniczy lublin SA"
    airportCode_ = "LUZ"

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

        tbody = data_.find("div",id="departures-table").find("div",role="table").find_all("div",recursive=False)[1]

        trs = tbody.find_all("div",recursive=False)

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("div",recursive=False)
            
            time = tds[0].get_text() or ''
            flight_ = Flight()
            flight_.time = time
            flight_.destination = tds[2].find("p").get_text() or ' '
            flight_.date = tds[1].get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.status = tds[5].get_text().split() or ' '
            carrierText = tds[4].find("img").get("alt") if tds[4].find("img") else "-"
            flight_.carrier = "-"
            if carrierText == "LO":
            
                flight_.carrier = "LOT"
            elif carrierText == "W6":
                flight_.carrier = "WIZZ AIR"
            elif carrierText == "FR":
                flight_.carrier = "RYANAIR"
            elif carrierText == "E4":
                flight_.carrier ="ENTER AIR"
            else:
                flight_.carrier = carrierText
            
            flight = flight_.to_dict()
            
            flights_info.append(flight) 
        return flights_info   

    def getArrivals(self):

        data = self.makeRequestHTML() 
        
        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("div",id="arrivals-table").find("div",role="table").find_all("div",recursive=False)[1]

        trs = tbody.find_all("div",recursive=False)

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("div",recursive=False)
            
            time = tds[0].get_text() or ''
            flight_ = Flight()

            flight_.time = time
            flight_.date = tds[1].get_text() or ' '
            flight_.origin = tds[2].find("p").get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.status = tds[5].get_text().split() or ' '
            carrierText = tds[4].find("img").get("alt") if tds[4].find("img") else "-";
            flight_.carrier = "-"
            if carrierText == "LO":
            
                flight_.carrier = "LOT"
            elif carrierText == "W6":
                flight_.carrier = "WIZZ AIR"
            elif carrierText == "FR":
                flight_.carrier = "RYANAIR"
            elif carrierText == "E4":
                flight_.carrier ="ENTER AIR"
            else:
                flight_.carrier = carrierText
            
            flight = flight_.to_dict()
            flights_info.append(flight) 
        return flights_info  