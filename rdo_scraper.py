from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class RDO_Scraper(BaseScraper):

    airportName_ = "Warsaw-Radom Airport"
    airportCode_ = "RDO"

    def __init__(self, url):
            super().__init__(url)
            print(f"{self.airportCode_} |  {self.airportName_} scraper - init")
            #super().printUrl()

    def makeRequestHTML(self,url=None, headers=None, method=None, json=None):

        header_ = headers or None
        method_ = method or None
        payload_ = json or None
        if url is None:
            url = self.url_
 
        result = super().makeRequestHTML(url, headers=header_,method=method_,json=payload_)
            
        return result


    def getArrivalsTableHeader(self):
        table_header = f"""
                <h>Arrivals: {self.airportName_}</h>
                <table border="1" style="border-collapse: collapse; width=100%; text-align:left;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="padding: 5px;">Time</th>
                            <th style="padding: 5px;">Destination</th> 
                            <th style="padding: 5px;">Carrier</th>
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
                                <th style="padding: 5px;">Carrier</th>
                                <th style="padding: 5px;">Flight Number</th>
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
    
            time = panel["arrivalTime"].strip() 
            destination = panel["destination"].strip() 
            number = panel["flightNum"].strip()
            carrier = panel["carrier"].strip()
            status = panel["status"].strip() 
    
            htmlText = f"""
            <tr>
                <td style="padding:5px;">{time}</td>
                <td style="padding:5px;">{destination}</td> 
                <td style="padding:5px;">{carrier}</td>
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
            carrier = flight["carrier"].strip()
            number = flight["flightNum"].strip() 
            status = flight["status"].strip()  
    
            htmlText = f"""
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 5px;">{time}</td>
                    <td style="padding: 5px;">{destination}</td>
                    <td style="padding: 5px;">{carrier}</td>
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

        data = ""
        print("downloading")

        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/json"
            }

        payload_ = {
            "flightNo":"",
            "origin":"",
            "airline":"",
            "time":"",
            "page":1,
            "locale":"pl",
            "type":"departures"
            }
        
        data = self.makeRequestHTML(headers=headers, method="POST", json=payload_ )  #(url=None, headers=None, method=None):
        print(data)
        data_ = data.json() 

        print(f"Found {len(data_["data"])} elements")

        flights_info = []
        for flight in data_["data"]:
 
            time = flight["scheduled_datetime_pl"] or '' 

            arrivaltime_ = time
            destination_ = flight["origin_en"] or ' '
            number = flight["flight_no"] or ' '
            carrier = flight["airline"] or ' '
            status = flight["status_en"] or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "carrier":carrier,
                "flightNum":number,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):

        data = ""
        print("downloading")

        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/json"
            }

        payload_ = {
            "flightNo":"",
            "origin":"",
            "airline":"",
            "time":"",
            "page":1,
            "locale":"pl",
            "type":"arrivals"
            }
        
        data = self.makeRequestHTML(headers=headers, method="POST", json=payload_ )  #(url=None, headers=None, method=None):
        print(data)
        data_ = data.json() 

        print(f"Found {len(data_["data"])} elements")

        flights_info = []
        for flight in data_["data"]:
 
            time = flight["scheduled_datetime_pl"] or ''

            arrivaltime_ = time
            destination_ = flight["origin_en"] or ' '
            number = flight["flight_no"] or ' '
            carrier = flight["airline"] or ' '
            status = flight["status_en"] or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "carrier":carrier,
                "flightNum":number,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info