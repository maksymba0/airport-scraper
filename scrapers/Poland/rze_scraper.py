from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timedelta
from flight import Flight, FlightFields

class RZE_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Rzeszów - Jasionka"
    airportCode_ = "RZE"

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

        tbody = data_.find("div",class_="table-responsive timetable-departures").find("tbody")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        today = datetime.now().date()
        current_date = today
        previous_time = None
        flights_info = []
        for tr in trs:

            tds = tr.find_all("td")
            if len(tds) < 3:
                continue
            time = tds[1].get_text() or ''

            
            time_obj = datetime.strptime(time, "%H:%M").time()
 
            if previous_time is not None and time_obj < previous_time:
                current_date += timedelta(days=1)
            flight_datetime = datetime.combine(current_date, time_obj).strftime("%d/%m/%Y")
            previous_time = time_obj

            flight_ = Flight()

            flight_.date = flight_datetime

            flight_.time = time
            flight_.destination = tds[2].get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.carrier = tds[0].find("img").get("alt","") if tds[0].find("img") else "-"
            flight_.status = tds[4].get_text() or ' '
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

        tbody = data_.find("div",class_="table-responsive timetable-arrivals").find("tbody")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []

        today = datetime.now().date()
        current_date = today
        previous_time = None

        for tr in trs:

            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            time = tds[1].get_text() or ''

            time_obj = datetime.strptime(time, "%H:%M").time()
 
            if previous_time is not None and time_obj < previous_time:
                current_date += timedelta(days=1)
            flight_datetime = datetime.combine(current_date, time_obj).strftime("%d/%m/%Y")

            previous_time = time_obj

            flight_ = Flight()

            flight_.date = flight_datetime
            flight_.time = time
            flight_.origin = tds[2].get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.carrier = tds[0].find("img").get("alt","") if tds[0].find("img") else "-"
            flight_.status = tds[4].get_text() or ' ' 
            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info