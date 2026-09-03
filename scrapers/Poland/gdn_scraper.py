from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class GDN_Scraper(BaseScraper):

    airportName_ = "Gdansk Lech Walesa Airport"
    airportCode_ = "GDN"

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
    
        data = self.makeRequestHTML("https://www.airport.gdansk.pl/loty/tablica-odlotow") 
        try:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        panel = _data.find('div', class_="table-schedule")
    
        rawData = panel['data-symfony--ux-react--react-props-value'] 
    
        PData = JSON.loads(rawData) 
        
        #print("Keys found in data:", PData.keys()) 
        # ['arrivals', 'departures', 'locale', 'fetchedDate', 'securityWaitTime', 'isMainPage', 'ticketsLink']
    
        departures = PData.get('departures')
         
        if not departures:
            print("Couldn't get departures")
            return []
        
        departures_list = JSON.loads(departures)  

        flights_info = []
        for flight in departures_list: 
   
            flight_ = Flight() 
            raw_time = flight["dateTime"].strip()
            dtTime = datetime.fromisoformat(raw_time)
            flight_.date = dtTime.strftime("%d/%m/%Y")
            flight_.time = dtTime.strftime("%H:%M")
            flight_.destination = flight["destination"].strip()
            flight_.carrier = flight["carrierName"].strip() 
            flight_.flightNum = flight["flight"].strip()
            flight_.status = flight["remarks"].strip()  
            flight_.terminal = flight.get("terminal") or ""
            
            flight_ = flight_.to_dict()
            
            flights_info.append(flight_) 
        return flights_info 
    def getArrivals(self):

        data = self.makeRequestHTML("https://www.airport.gdansk.pl/loty/tablica-przylotow") 
        try:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        panel = _data.find('div', class_="table-schedule")
    
        rawData = panel['data-symfony--ux-react--react-props-value'] 
    
        PData = JSON.loads(rawData)
 
      
       # print("Keys found in data:", PData.keys()) 
        # ['arrivals', 'departures', 'locale', 'fetchedDate', 'securityWaitTime', 'isMainPage', 'ticketsLink']
    
        arrivals = PData.get('arrivals')
        if not arrivals:
            print("Couldn't get arrivals")
            return []
        
        arrivals_list = JSON.loads(arrivals) 

        flights_info = []
        for flight in arrivals_list: 
    
            flight_ = Flight()

            raw_time = flight["dateTime"].strip()
            dtTime = datetime.fromisoformat(raw_time)
            flight_.date = dtTime.strftime("%d/%m/%Y")
            flight_.time = dtTime.strftime("%H:%M")
            flight_.origin = flight["origin"].strip()
            flight_.carrier = flight["carrierName"].strip() 
            flight_.flightNum = flight["flight"].strip()
            flight_.status = flight["remarks"].strip() 
            flight_.gate = flight.get("terminal") or ""
            
            flight_ = flight_.to_dict()

            flights_info.append(flight_) 
        return flights_info

    #   DEPARTURES
    # {
    # 'destination': 'KATANIA', 
    # 'gate': '17,18', 
    # 'autoCh': True, 
    # 'currDisp': None, 
    # 'landingTime': None,
    #  'visible': True, 
    # 'remarks': 'opózniony 22:20',
    #  'dateTime': '2026-08-11T19:15:00+02:00',
    #  'carrierName': 'WIZZ AIR',
    #  'expectedDateTime': '2026-08-11T22:20:00+02:00', 
    # 'delayedDescription': None, 
    # 'terminal': None, 
    # 'cFlight': None,
    #  'local': False,
    #  'flight': 'W6 1685',
    #  'remarksStatus': 3}


    #   ARRIVALS
    # {'origin': 'OSLO GARDERMOEN', 
    # 'remarks': 'wylądował', 
    # 'dateTime': '2026-08-11T18:55:00+02:00', 
    # 'carrierName': 'WIZZ AIR', 
    # 'expectedDateTime': '2026-08-11T19:50:00+02:00', 
    # 'delayedDescription': None, 
    # 'terminal': None, 
    # 'cFlight': None, 
    # 'local': False, 
    # 'flight': 'W6 1786',
    #  'remarksStatus': 2}