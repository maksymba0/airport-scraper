from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime, timedelta
from flight import Flight, FlightFields
import re

class WMI_Scraper(BaseScraper):

    airportName_ = "Warsaw Modlin Airport"
    airportCode_ = "WMI"

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
    
        data = self.makeRequestHTML("https://www.jakdolece.pl/rozklad-lotow/warszawa-modlin-wmi/odloty") 
        try:
            _data = bs(data,"html.parser")
        except Exception:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []


        flights_list = _data.find('section', class_="about-us pt-0 pb-6 schedule").find('div',class_='container').find('tbody');

        trs = flights_list.find_all("tr",recursive=False); 

        print(f"Found {len(trs)} elements")

        flights_info = []

        today = datetime.today()
        currentdate = today
        previous = None

        for tr in trs: 

            if not tr.has_attr('class'):
                continue
            header = tr.find('th')
            if not header:
                continue
            label = header.get('data-label','').strip() 
            if not label:
                continue

            tds = tr.find_all('td')

            flight = Flight()

            flight.time = header.text.strip();
            match = re.search(r'(\d{2}:\d{2})', flight.time)
            flight.time = match.group(1) if match else flight.time

            timeobj = datetime.strptime(flight.time,"%H:%M").time()

            if previous is not None and timeobj < currentdate.strptime("%H:%M"):
                currentdate += timedelta(days=1)

            flight.date = datetime.combine(currentdate,timeobj).strftime("%d/%m/%Y")

            flight.destination = tds[0].find('a').text or ''
            flight.flightNum = tds[1].text or '';
            flight.carrier = tds[2].find('img').get('alt','');

            flight.status = tds[3].get('status','');
            value =  re.search(r'gate\s+(\d+)',flight.status,re.IGNORECASE)  
            flight.gate = value.group(1) if value else None 
            dFlight = flight.to_dict()
            flights_info.append(dFlight)
            
        return flights_info  
        
    def getArrivals(self):

        print("downloading")
        data = self.makeRequestHTML("https://www.jakdolece.pl/rozklad-lotow/warszawa-modlin-wmi/przyloty") 
        try:
            _data = bs(data,"html.parser")
        except Exception:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []
 
        flights_list = _data.find('section', class_="about-us pt-0 pb-6 schedule").find('div',class_='container').find('tbody');

        trs = flights_list.find_all("tr",recursive=False); 

        print(f"Found {len(trs)} elements")

        flights_info = []

        today = datetime.today()
        currentdate = today
        previous = None
         
        for tr in trs: 

            if not tr.has_attr('class'):
                continue
            header = tr.find('th')
            if not header:
                continue
            label = header.get('data-label','').strip() 
            if not label:
                continue

            tds = tr.find_all('td')

            flight = Flight()

            flight.time = header.text.strip();
            match = re.search(r'(\d{2}:\d{2})', flight.time)
            flight.time = match.group(1) if match else flight.time
             

            timeobj = datetime.strptime(flight.time,"%H:%M").time()

            if previous is not None and timeobj < currentdate.strptime("%H:%M"):
                currentdate += timedelta(days=1)

            flight.date = datetime.combine(currentdate,timeobj).strftime("%d/%m/%Y")

            flight.origin = tds[0].find('a').text or ''
            flight.flightNum = tds[1].text or '';
            flight.carrier = tds[2].find('img').get('alt','');

            flight.status = tds[3].get('status','');
            value =  re.search(r'gate\s+(\d+)',flight.status,re.IGNORECASE)  
            flight.gate = value.group(1) if value else None 
            dFlight = flight.to_dict()
            flights_info.append(dFlight)
            
        return flights_info 