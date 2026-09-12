from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timedelta
from flight import Flight, FlightFields
import cloudscraper as CloudScrapper



class WRO_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Wrocław SA"
    airportCode_ = "WRO"

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

        print("downloading")
        scrapper = CloudScrapper.create_scraper(browser={
            'browser':'chrome',
            'platform':'windows',
            'desktop':True
        })
        data = scrapper.get(self.url_) 

        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        flightsTable = _data.find('div', id="departures")

        flightsBody = flightsTable.find("table", class_="flight-table",recursive=False).find("tbody")

        trs = flightsBody.find_all("tr")


        flights = []

        today = datetime.today()
        currentdate = today
        previous = None

        for tr in trs:
            className = tr.get("class", []) # Safely get class list
            if "flight-info-popup-row" in className:
                continue   
            tds = tr.find_all("td")
            flightTime = tds[0].get_text(strip=True)

            timeobj = datetime.strptime(flightTime,"%H:%M").time()

            if previous is not None and previous < timeobj:
                currentdate += timedelta(days=1)

            flightdate_ = datetime.combine(currentdate, timeobj).strftime("%d/%m/%Y")

            airport = tds[1].find_all("div")[0].get_text(strip=True)
            flight_no = tds[2].get_text(strip=True)
            status = tds[3].get_text(strip=True)
            carriertext = flight_no
           
            flight_ = Flight()
            
            flight_.time= flightTime
            flight_.destination = airport
            flight_.date = flightdate_
            flight_.flightNum = flight_no
            flight_.carrier = carriertext if (airline := flight_.findAirline()) == '-' else airline
            flight_.status = status 
            flight_.country = 'PL'
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
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []
 



        flightsTable = _data.find('div', id="arrivals")

        
        flightsBody = flightsTable.find("table", class_="flight-table",recursive=False).find("tbody")

        trs = flightsBody.find_all("tr")

    
        flights = []
        today = datetime.today()
        currentdate = today
        previous = None
        for tr in trs:
            className = tr.get("class", []) # Safely get class list
            if "flight-info-popup-row" in className:
                continue   
            tds = tr.find_all("td")

            flightTime = tds[0].get_text(strip=True)

            timeobj = datetime.strptime(flightTime,"%H:%M").time()

            if previous is not None and previous < timeobj:
                currentdate += timedelta(days=1)

            flightdate_ = datetime.combine(currentdate, timeobj).strftime("%d/%m/%Y")

            airport = tds[1].find_all("div")[0].get_text(strip=True)
            flight_no = tds[2].get_text(strip=True)
            status = tds[3].get_text(strip=True) 
            carriertext = flight_no 
            flight_ = Flight()

            flight_.time= flightTime
            flight_.date = flightdate_
            flight_.origin = airport
            flight_.flightNum = flight_no
            flight_.carrier = carriertext if (airline := flight_.findAirline()) == '-' else airline
            flight_.status = status 
            flight_.country = 'PL'
            flight = flight_.to_dict() 
 
            
            flights.append(flight)
 
        print(f"Found {len(flights)} elements")
        return flights 