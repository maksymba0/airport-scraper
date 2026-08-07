from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class LCJ_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Łódź im. Władysława Reymonta Sp. z o.o."
    airportCode_ = "LCJ"

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
    
            time = panel[FlightFields.arrivalTime].strip() 
            destination = panel[FlightFields.destination].strip() 
            number = panel[FlightFields.number].strip()
            status = panel[FlightFields.status].strip() 
    
            htmlText = f"""
            <tr>
                <td style="padding:5px;">{time}</td>
                <td style="padding:5px;">{destination}</td> 
                <td style="padding:5px;">{number}</td>
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
            time = flight["arrivalTime"].strip() 
            destination = flight["destination"].strip() 
            number = flight["flightNum"].strip() 
            status = flight["status"].strip()  
    
            htmlText = f"""
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 5px;">{time}</td>
                    <td style="padding: 5px;">{destination}</td>
                    <td style="padding: 5px;">{number}</td>
                    <td style="padding: 5px;">{status}</td>
                </tr>
            """
            departures_rows.append(htmlText)
        departures_text = "".join(departures_rows)
        htmlfooter = "</tbody></table>"
        content = topHeader + departures_text + htmlfooter
        return content 


    def getDepartures(self):

        data = self.makeRequestHTML() 

        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("tbody",class_="timetableDepartures")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("td")
                       
            time = tds[0].get_text().split() or ''

            arrivaltime_ = time[2] #08.08.2026 - 08:25
            destination_ = tds[1].get_text() or ' '
            number = tds[2].get_text() or ' '
            status = tds[3].get_text() or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "flightNum":number,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info   

    def getArrivals(self):

        data = ""
        print("downloading")
        data = self.makeRequestHTML()  

        _data = data.text
 

        data_ = bs(_data,"html.parser")

        tbody = data_.find("tbody",class_="timetableArrivals")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("td")
            
            time = tds[0].get_text().split() or ''

            arrivaltime_ = time[2] #08.08.2026 - 08:25
            destination_ = tds[1].get_text() or ' '
            number = tds[2].get_text() or ' '
            status = tds[3].get_text() or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "flightNum":number,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info  