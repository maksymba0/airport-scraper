from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime,timedelta
from flight import Flight, FlightFields
import cloudscraper as CloudScrapper




class SZZ_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Szczecin Goleniów"
    airportCode_ = "SZZ"

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
        data = ""
        print("downloading")
        scrapper = CloudScrapper.create_scraper(browser={
            'browser':'chrome',
            'platform':'windows',
            'desktop':True
        })
        data = scrapper.get(self.url_) 
        try:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []



        flightsTable = _data.find('div', id="departuresInfo")

        flightsBody = flightsTable.find("tbody")

        trs = flightsBody.find_all("tr")


        flights = []

        today = datetime.now().date()
        current_date = today
        previous_time = None

        for tr in trs: 
            tds = tr.find_all("td")

            flight_ = Flight()
            
            flight_.time = tds[0].get_text(strip=True)

            time_obj = datetime.strptime(flight_.time, "%H:%M").time()
            
            if previous_time is not None and time_obj < previous_time:
                current_date += timedelta(days=1)

            flight_datetime = datetime.combine(current_date, time_obj).strftime("%d/%m/%Y")
            previous_time = time_obj

            flight_.date = flight_datetime

            flight_.destination = tds[2].get_text(strip=True)
            flight_.flightNum = tds[1].get_text(strip=True)
            flight_.status = tds[3].get_text(strip=True)
            carriertext = flight_.flightNum
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
            flights.append(flight)

        print(f"Found {len(trs)} elements")
        return flights 
    def getArrivals(self):
 
        print("downloading")
        scrapper = CloudScrapper.create_scraper(browser={
            'browser':'chrome',
            'platform':'windows',
            'desktop':True
        })
        data = scrapper.get(self.url_) 
             
        try:
           _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return [] 


        flightsTable = _data.find('div', id="arrivalsInfo")
        
        flightsBody = flightsTable.find("tbody")

        trs = flightsBody.find_all("tr")

    
        flights = []
        today = datetime.now().date()
        current_date = today
        previous_time = None

        for tr in trs: 
            tds = tr.find_all("td")
            flight_ = Flight()
            flight_.time = tds[0].get_text(strip=True)

            time_obj = datetime.strptime(flight_.time, "%H:%M").time()
            
            if previous_time is not None and time_obj < previous_time:
                current_date += timedelta(days=1)

            flight_datetime = datetime.combine(current_date, time_obj).strftime("%d/%m/%Y")
            previous_time = time_obj

            flight_.date = flight_datetime



            flight_.destination = tds[2].get_text(strip=True)
            flight_.flightNum = tds[1].get_text(strip=True)
            flight_.status = tds[3].get_text(strip=True)
            carriertext = flight_.flightNum
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

            flights.append(flight)
        
        print(f"Found {len(flights)} elements")
        return flights 