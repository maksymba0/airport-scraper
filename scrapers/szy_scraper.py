from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class SZY_Scraper(BaseScraper):

    airportName_ = "PORT LOTNICZY OLSZTYN - MAZURY"
    airportCode_ = "SZY"

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

        data = self.makeRequestHTML() 

        _data = data.text
        
        
        data_ = bs(_data,"html.parser")
   
        tbody = data_.find("div",id="header-timetable").find_all("table")[1]

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs[1:]:

            tds = tr.find_all("td") 

            time = tds[0].get_text().split() or ''
            flight_ = Flight()
            
            flight_.time = time[2] 
            destt = " ".join(tds[2].get_text().split())
            flight_.destination = destt or ' '
            text = tds[1].get_text().split()
            flight_.flightNum = f"{text[1]} {text[2]}".replace("(","").replace(")","")
            flight_.carrier = text[0]
            flight_.status = tds[3].get_text() or ' '
            flight = flight_.to_dict()
            
            flights_info.append(flight) 
        return flights_info

    def getArrivals(self):

        data = ""
        print("downloading")
        data = self.makeRequestHTML()  

        _data = data.text
        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("div",id="header-timetable").find_all("table")[0]

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs[1:]:

            tds = tr.find_all("td") 

            time = tds[0].get_text().split() or ''

            flight_ = Flight()

            flight_.time = time[2] 
            destt = " ".join(tds[2].get_text().split())
            flight_.origin = destt or ' '
            text = tds[1].get_text().split()
            flight_.flightNum = f"{text[1]} {text[2]}".replace("(","").replace(")","")
            carriertext = text[0]
            flight_.carrier = ""
            if "RR" in carriertext:
                flight_.carrier = "RYANAIR"
            elif "LO" in carriertext:
                flight_.carrier = "LOT"
            elif "W6" in carriertext:
                flight_.carrier = "WIZZ AIR"
            elif "FR" in carriertext:
                flight_.carrier ="RYANAIR"
            else:
                flight_.carrier = carriertext

            flight = flight_.to_dict()

            flights_info.append(flight) 
        return flights_info