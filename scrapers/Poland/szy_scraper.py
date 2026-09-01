from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class SZY_Scraper(BaseScraper):

    airportName_ = "PORT LOTNICZY OLSZTYN - MAZURY"
    airportCode_ = "SZY"

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
   
        tbody = data_.find("div",id="header-timetable").find_all("table")[1]

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs[1:]:

            tds = tr.find_all("td") 

            time = tds[0].get_text().split() or ''
            flight_ = Flight()
            
            flight_.time = time[2] 
            flight_.date = time[0].replace('.','/').replace('-','/') 
            destt = " ".join(tds[2].get_text().split())
            flight_.destination = destt or ' '
            text = tds[1].get_text().split()
            flight_.flightNum = f"{text[1]} {text[2]}".replace("(","").replace(")","")
            flight_.carrier = text[0]
            flight_.status = tds[3].get_text() or ' '
            flight = flight_.to_dict()
            
            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):

        data = ""
        print("downloading")
        data = self.makeRequestHTML()  

        _data = data.text
        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("div",id="header-timetable").find_all("table")[0]

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs[1:]:

            tds = tr.find_all("td") 

            time = tds[0].get_text().split() or ''

            flight_ = Flight()

            flight_.time = time[2] 
            flight_.date = time[0].replace('.','/').replace('-','/') 
            destt = " ".join(tds[2].get_text().split())
            flight_.origin = destt or ' '
            text = tds[1].get_text().split()
            flight_.flightNum = f"{text[1]} {text[2]}".replace("(","").replace(")","")
            carriertext = text[0]
            flight_.carrier = ""
            if "RR" in carriertext:
                flight_.carrier = "RYANAIR"
            elif "LO" in carriertext:
                flight_.carrier = "LOT"
            elif "W6" in carriertext:
                flight_.carrier = "WIZZ AIR"
            elif "FR" in carriertext:
                flight_.carrier ="RYANAIR"
            else:
                flight_.carrier = carriertext

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info