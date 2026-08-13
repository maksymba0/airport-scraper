from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
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
        for li in flights[1:]: 

            flight = Flight()
            
            flight.time = t.get_text(strip=True) if (t := li.select_one(".column-time.arrivals-col")) else ""
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
        for li in flights[1:]: 

            arrivaltime_ = t.get_text(strip=True) if (t := li.select_one(".column-time.arrivals-col")) else ""
            destination_ = t.get_text(strip=True) if (t := li.select_one(".column-origin-destination")) else ""
            number = t.get_text(strip=True) if (t := li.select_one(".column-flight-no")) else ""
            carrier = t.get("alt","") if (t := li.select_one(".column-airline img")) else ""
            gate = t.get_text(strip=True) if (t := li.select_one(".column-gate")) else ""
            status = t.get_text(strip=True) if (t := li.select_one(".column-status")) else ""
            flight_ = Flight()

            flight_.carrier = carrier
            flight_.time = arrivaltime_
            flight_.origin = destination_
            flight_.flightNum = number
            flight_.status = status
            flight_.gate = gate
            flight = flight_.to_dict()  
        
            flights_info.append(flight) 
        return flights_info  