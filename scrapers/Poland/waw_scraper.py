from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timedelta
from flight import Flight, FlightFields

class WAW_Scraper(BaseScraper):

    airportName_ = "Warsaw Chopin Airport"
    airportCode_ = "WAW"

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
    
        data = self.makeRequestHTML("https://lotnisko-chopina.pl/pl/przyloty-i-odloty/?operation=d") 
        try:
            _data = bs(data,"html.parser")
        except Exception:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []


        flights_list = _data.find('ul', class_="flights-list")

        flights = flights_list.find_all("li",class_="arrivals-departures-tables") 

        print(f"Found {len(flights)} elements")

        flights_info = []

        today = datetime.today()
        currentdate = today
        previous = None

        for li in flights[1:]: 

            flight = Flight()

            flight.time = t.get_text(strip=True) if (t := li.select_one(".column-time.arrivals-col")) else ""

            timeobj = datetime.strptime(flight.time,"%H:%M").time()

            if previous is not None and timeobj < currentdate.strptime("%H:%M"):
                currentdate += timedelta(days=1)

            flight.date = datetime.combine(currentdate,timeobj).strftime("%d/%m/%Y")

            flight.destination = t.get_text(strip=True) if (t := li.select_one(".column-origin-destination")) else ""
            flight.flightNum = t.get_text(strip=True) if (t := li.select_one(".column-flight-no")) else ""
            flight.carrier = t.get("alt","") if (t := li.select_one(".column-airline img")) else ""
            flight.gate = t.get_text(strip=True) if (t := li.select_one(".column-gate")) else ""
            flight.status = t.get_text(strip=True) if (t := li.select_one(".column-status")) else ""
            dFlight = flight.to_dict()
            flights_info.append(dFlight)
            
        return flights_info  
        
    def getArrivals(self):

        print("downloading")
        data = self.makeRequestHTML("https://lotnisko-chopina.pl/pl/przyloty-i-odloty/?operation=a") 
        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []


        flights_list = _data.find('ul', class_="flights-list")

        flights = flights_list.find_all("li",class_="arrivals-departures-tables") 

        print(f"Found {len(flights)} elements")

        flights_info = []
        today = datetime.today()
        currentdate = today
        previous = None

        for li in flights[1:]: 

            arrivaltime_ = t.get_text(strip=True) if (t := li.select_one(".column-time.arrivals-col")) else ""
            destination_ = t.get_text(strip=True) if (t := li.select_one(".column-origin-destination")) else ""
            number = t.get_text(strip=True) if (t := li.select_one(".column-flight-no")) else ""
            carrier = t.get("alt","") if (t := li.select_one(".column-airline img")) else ""
            gate = t.get_text(strip=True) if (t := li.select_one(".column-gate")) else ""
            status = t.get_text(strip=True) if (t := li.select_one(".column-status")) else ""
            flight_ = Flight()

            timeobj = datetime.strptime(arrivaltime_,"%H:%M").time()

            if previous is not None and timeobj < currentdate.strptime("%H:%M"):
                currentdate += timedelta(days=1)

            flight_.date = datetime.combine(currentdate,timeobj).strftime("%d/%m/%Y")

            flight_.carrier = carrier
            flight_.time = arrivaltime_
            flight_.origin = destination_
            flight_.flightNum = number
            flight_.status = status
            flight_.gate = gate
            flight = flight_.to_dict()  
        
            flights_info.append(flight) 
        return flights_info  