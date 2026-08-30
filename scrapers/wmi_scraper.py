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


    def getArrivalsTableHeader(self):
        table_header = f"""
                 <h>Arrivals: {self.airportName_}</h>
                <table border="1" style="border-collapse: collapse; width=100%; text-align:left;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="padding: 5px;">Time</th>
                            <th style="padding: 5px;">Destination</th> 
                            <th style="padding: 5px;">Flight Number</th>
                            <th style="padding: 5px;">Carrier</th>
                            <th style="padding: 5px;">Gate</th>
                            <th style="padding: 5px;">Status</th>
                        </tr>
                    </thead> 
                    <tbody>
                """
        return table_header
    def getDeparturesTableHeader(self):
        table_header = f"""
                 <h>Departures: {self.airportName_}</h>
                    <table border="1" style="border-collapse: collapse; width=100%; text-align:left;">
                        <thead>
                            <tr style="background-color: #f2f2f2;">
                                <th style="padding: 5px;">Time</th>
                                <th style="padding: 5px;">Destination</th> 
                                <th style="padding: 5px;">Flight Number</th>
                                <th style="padding: 5px;">Gate</th>
                                <th style="padding: 5px;">Status</th>
                            </tr>
                        </thead> 
                        <tbody>
                """
        return table_header
    def getArrivalsTable(self):

        flights = self.getArrivals() 
        #"arrivalTime": arrivaltime_,
        #"destination":destination_,
        #"flightNum":number,
        #"gate":gate
        print("Flight data: \n")
        
        table_header = self.getArrivalsTableHeader()
    
        flights_text = []
        for panel in flights:
    
            time = panel[FlightFields.arrivalTime].strip() 
            destination = panel[FlightFields.destination].strip() 
            number = panel[FlightFields.number].strip()
            gate = panel[FlightFields.gate].strip() 
            status = panel[FlightFields.status].strip() 
            carrier = panel[FlightFields.carrier].strip()
    
            htmlText = f"""
            <tr>
                <td style="padding:5px;">{time}</td>
                <td style="padding:5px;">{destination}</td> 
                <td style="padding:5px;">{number}</td>
                <td style="padding:5px;">{carrier}</td>
                <td style="padding:5px;">{gate}</td>
                <td style="padding:5px;">{status}</td>
            </tr>
            """
    
            flights_text.append(htmlText) 
        table_body = "".join(flights_text)
        table_footer = "</tbody></table>"
        
        content = table_header + table_body + table_footer
    
        return content

    def getDeparturesAsTable(self):
        departures_list = self.getDepartures()

        topHeader = self.getDeparturesTableHeader()

        departures_rows = []
        for flight in departures_list:
            time = flight[FlightFields.arrivalTime].strip()  
            destination = flight[FlightFields.destination].strip()
            carrier = flight[FlightFields.carrier].strip() 
            number = flight[FlightFields.number].strip()
            status = flight[FlightFields.status].strip() 
            gate = flight[FlightFields.gate] or "" 
    
            htmlText = f"""
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 5px;">{time}</td>
                    <td style="padding: 5px;">{destination}</td>
                    <td style="padding: 5px;">{carrier}</td>
                    <td style="padding: 5px;">{number}</td>
                    <td style="padding: 5px;">{gate}</td>
                    <td style="padding: 5px;">{status}</td>
                </tr>
            """
            departures_rows.append(htmlText)
        departures_text = "".join(departures_rows)
        htmlfooter = "</tbody></table>"
        content = topHeader + departures_text + htmlfooter
        return content 


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
            print(flight.time)

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