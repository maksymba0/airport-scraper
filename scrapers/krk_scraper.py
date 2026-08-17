from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class KRK_Scraper(BaseScraper):

    airportName_ = "Kraków Airport"
    airportCode_ = "KRK"

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
                            <th style="padding: 5px;">IATA Code</th>
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
                                    <th style="padding: 5px;">Carrier</th>
                                    <th style="padding: 5px;">Status</th>
                                </tr>
                            </thead> 
                            <tbody>
                        """
        return table_header
    def getArrivalsTable(self):

        flights = self.getArrivals()  

        print("Flight data: \n")
        
        table_header = self.getArrivalsTableHeader()
    
        flights_text = []
        for panel in flights:
    
            time = panel["arrivalTime"].strip() 
            origin = panel["Origin"].strip() 
            number = panel["flightNum"].strip()
            gate = panel["gate"].strip() 
            status = panel["status"].strip() 
            carrier = panel["carrier"].strip()
    
            htmlText = f"""
            <tr>
                <td style="padding:5px;">{time}</td>
                <td style="padding:5px;">{origin}</td> 
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

        flights = self.getDepartures()  

        print("Flight data: \n")
        
        table_header = self.getDeparturesTableHeader()
    
        flights_text = []
        for panel in flights:
    
            time = panel["arrivalTime"].strip() 
            destination = panel["destination"].strip() 
            number = panel["flightNum"].strip()
            status = panel["status"].strip() 
            carrier = panel["carrier"].strip()
    
            htmlText = f"""
            <tr>
                <td style="padding:5px;">{time}</td>
                <td style="padding:5px;">{destination}</td> 
                <td style="padding:5px;">{number}</td>
                <td style="padding:5px;">{carrier}</td>
                <td style="padding:5px;">{status}</td>
            </tr>
            """
    
            flights_text.append(htmlText) 
        table_body = "".join(flights_text)
        table_footer = "</tbody></table>"
        
        content = table_header + table_body + table_footer

        return content


    def getDepartures(self):

        print("downloading")
        data = self.makeRequestHTML("https://krakowairport.pl/pl/pasazer/loty/polaczenia/odloty") 
             
        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []
 

        departures_table = _data.find('div', class_="departures_table") 

        value = departures_table.get("wire:snapshot") 

        jsonValues = JSON.loads(value) 

        print(f"Found {len(jsonValues["data"]["flights"][0])} elements")

        flights_info = []
        flights = jsonValues["data"]["flights"][0]
        for fl in flights: 

            flight_ = Flight()

            flight_.date = fl[0]["scheduled_date"].strip() if fl[0]["scheduled_date"] else ""
            flight_.time = fl[0]["scheduled_time"].strip() if fl[0]["scheduled_time"] else ""
            flight_.origin = fl[0]["origin"].strip() if fl[0]["origin"] else ""
            flight_.destination = fl[0]["destination"].strip() if fl[0]["destination"] else ""
            flight_.flightNum = fl[0]["flight_no"].strip() if fl[0]["flight_no"] else ""
            flight_.carrier =fl[0]["airline"].strip() if fl[0]["airline"] else ""
            flight_.gate = fl[0]["gate_id"].strip() if fl[0]["gate_id"] else ""
            flight_.terminal = fl[0]["terminal"].strip() if fl[0]["terminal"] else ""
            flight_.status = fl[0]["remarks"].strip() if fl[0]["remarks"] else ""
            flight = flight_.to_dict()

            flights_info.append(flight) 
 
        return flights_info   
    
    def getArrivals(self):

        print("downloading")
        data = self.makeRequestHTML() 
        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        departures_table = _data.find('div', class_="departures_table") 

        value = departures_table.get("wire:snapshot")
 
        jsonValues = JSON.loads(value) 

        print(f"Found {len(jsonValues["data"]["flights"][0])} elements")

        flights_info = []
        flights = jsonValues["data"]["flights"][0]
        for fl in flights: 

            flight_ = Flight()

            flight_.date = fl[0]["scheduled_date"].strip() if fl[0]["scheduled_date"] else ""
            flight_.time = fl[0]["scheduled_time"].strip() if fl[0]["scheduled_time"] else ""
            flight_.origin = fl[0]["origin"].strip() if fl[0]["origin"] else ""
            flight_.destination = fl[0]["destination"].strip() if fl[0]["destination"] else ""
            flight_.flightNum = fl[0]["flight_no"].strip() if fl[0]["flight_no"] else ""
            flight_.carrier =fl[0]["airline"].strip() if fl[0]["airline"] else ""
            flight_.gate = fl[0]["gate_id"].strip() if fl[0]["gate_id"] else ""
            flight_.terminal = fl[0]["terminal"].strip() if fl[0]["terminal"] else ""
            flight_.status = fl[0]["remarks"].strip() if fl[0]["remarks"] else ""
            flight = flight_.to_dict()
            
            flights_info.append(flight)
             
        return flights_info  

# 'id', 
# 'flight_id', 
# 'flight_no', 
# 'scheduled_datetime_pl', 
# 'scheduled_date', 
# 'scheduled_time', 
# 'expected_date', 
# 'expected_time', 
# 'airline', 
# 'airline_icao', 
# 'delayed', 
# 'delay', 
# 'terminal', 
# 'boarding', 
# 'check_in', 
# 'check_in_no', 
# 'gate_id', 
# 'origin_id', 
# 'origin', 
# 'origin_iata', 
# 'destination_id', 
# 'destination', 
# 'destination_iata', 
# 'is_arrival', 
# 'is_cancelled', 
# 'arrival_datetime_pl', 
# 'remarks_pl', 
# 'remarks'