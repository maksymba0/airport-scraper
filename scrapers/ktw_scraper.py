from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class KTW_Scraper(BaseScraper):

    airportName_ = "Katowice Airport"
    airportCode_ = "KTW"

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
                                <th style="padding: 5px;">Carrier</th>
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
    
            time = panel[FlightFields.time].strip() 
            destination = panel[FlightFields.origin].strip() 
            number = panel[FlightFields.flightNum].strip()
            gate = panel[FlightFields.terminal].strip() 
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
            time = flight[Flight].strip() 
            destination = flight["destination"].strip() 
            number = flight["flightNum"].strip()
            gate = flight["gate"].strip() 
            status = flight["status"].strip() 
            carrier = flight["carrier"].strip()
    
            htmlText = f"""
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 5px;">{time}</td>
                    <td style="padding: 5px;">{destination}</td>
                    <td style="padding: 5px;">{number}</td>
                    <td style="padding: 5px;">{carrier}</td>
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

        dateToday = datetime.today().strftime("%Y-%m-%d")
        data = self.makeRequestHTML(f"https://www.katowice-airport.com/pl/api/flight-board/list?direction=1&date={dateToday}&time_from=00:00&time_to=23:59") 

        _data = data
 

        data_ = JSON.loads(_data.text)
           
        flights_info = []
        
        dateNow = datetime.today().strftime("%d/%m/%Y")

        for key in data_['data']: 


            time = key['scheduled_time'] or ''

            flight_ = Flight()
            
            time = key['scheduled_time'] or ''

            flight_.date = dateNow
            flight_.time = time
            flight_.destination = key['airport'] or ' '
            flight_.flightNum = key['flight_number'] or ' '
            flight_.carrier = key['airline_name'] or ' '
            flight_.gate = key['boarding_gate'] or ' '
            flight_.status = key['status'] or ' '


            flight =  flight_.to_dict()
            flights_info.append(flight) 
        return flights_info  

    def getArrivals(self):

        data = ""
        print("downloading") 
        dateToday = datetime.today().strftime("%Y-%m-%d")
        data = self.makeRequestHTML(f"https://www.katowice-airport.com/pl/api/flight-board/list?direction=2&date={dateToday}&time_from=00:00&time_to=23:59")  

        _data = data.text
 

        data_ = JSON.loads(_data)
         

        print(f"Found {len(data_)} elements")

        flights_info = []
        dateNow = datetime.today().strftime("%d/%m/%Y")
        for key in data_['data']: 


            flight_ = Flight()
            
            time = key['scheduled_time'] or ''

            flight_.date = dateNow
            flight_.time = time
            flight_.origin = key['airport'] or ' '
            flight_.flightNum = key['flight_number'] or ' '
            flight_.carrier = key['airline_name'] or ' '
            flight_.terminal = key['boarding_gate'] or ' '
            flight_.status = key['status'] or ' '


            flight =  flight_.to_dict()

            flights_info.append(flight) 
        return flights_info  