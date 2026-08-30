from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class RDO_Scraper(BaseScraper):

    airportName_ = "Warsaw-Radom Airport"
    airportCode_ = "RDO"

    def __init__(self, url):
            super().__init__(url)
            print(f"{self.airportCode_} |  {self.airportName_} scraper - init")
            #super().printUrl()

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

        payload_ = {
            "flightNo":"",
            "origin":"",
            "airline":"",
            "time":"",
            "page":1,
            "locale":"pl",
            "type":"departures"
            }
        
        data = self.makeRequestHTML(headers=headers, method="POST", json=payload_ )  #(url=None, headers=None, method=None):
        
        data_ = data.json() 

        print(f"Found {len(data_["data"])} elements")

        flights_info = []
        for flight in data_["data"]:
 
            time = flight["scheduled_datetime_pl"].split() or ''

            flight_ = Flight()

            flight_.time = time[1]
            
            date = datetime.strptime(flight["scheduled_date_pl"],"%Y-%m-%d").strftime("%d/%m/%Y") or ' '
           
            flight_.date = date
            flight_.destination = flight["destination"] or ' '
            flight_.flightNum = flight["flight_no"] or ' '
            flight_.carrier = flight["airline"] or ' '
            flight_.status = flight["status_en"] or ' '
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

        payload_ = {
            "flightNo":"",
            "origin":"",
            "airline":"",
            "time":"",
            "page":1,
            "locale":"pl",
            "type":"arrivals"
            }
        
        data = self.makeRequestHTML(headers=headers, method="POST", json=payload_ )  #(url=None, headers=None, method=None):
       
        data_ = data.json() 

        print(f"Found {len(data_["data"])} elements")

        flights_info = []
        for flight in data_["data"]:
 
            time = flight["scheduled_datetime_pl"].split() or ''

            flight_ = Flight()

            flight_.time = time[1]
            date = datetime.strptime(flight["scheduled_date_pl"],"%Y-%m-%d").strftime("%d/%m/%Y") or ' '

            flight_.date = date
            flight_.origin = flight["origin_en"] or ' '
            flight_.flightNum = flight["flight_no"] or ' '
            flight_.carrier = flight["airline"] or ' '
            flight_.status = flight["status_en"] or ' '
            flight = flight_.to_dict()
            
            flights_info.append(flight) 
        return flights_info