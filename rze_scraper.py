from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class RZE_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Rzeszów - Jasionka"
    airportCode_ = "RZE"

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
            carrier = panel[FlightFields.carrier].strip()
            status = panel[FlightFields.status].strip() 
    
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
            time = flight[FlightFields.arrivalTime].strip() 
            destination = flight[FlightFields.destination].strip() 
            carrier = flight[FlightFields.carrier].strip()
            number = flight[FlightFields.number].strip() 
            status = flight[FlightFields.status].strip()  
    
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

        tbody = data_.find("div",class_="table-responsive timetable-departures").find("tbody")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs:

            tds = tr.find_all("td")
            if len(tds) < 3:
                continue
            time = tds[1].get_text() or ''

            arrivaltime_ = time
            destination_ = tds[2].get_text() or ' '
            number = tds[3].get_text() or ' '
            carrier = tds[0].find("img").get("alt","") if tds[0].find("img") else "-"
            status = tds[4].get_text() or ' '
            flight = {
                FlightFields.arrivalTime: arrivaltime_,
                FlightFields.destination:destination_,
                FlightFields.carrier:carrier,
                FlightFields.number:number,
                FlightFields.status:status
            }
            flights_info.append(flight) 
        return flights_info   

    def getArrivals(self):

        data = ""
        print("downloading")
        data = self.makeRequestHTML()  

        _data = data.text
        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("div",class_="table-responsive timetable-arrivals").find("tbody")

        trs = tbody.find_all("tr")

        print(f"Found {len(data_)} elements")

        flights_info = []
        for tr in trs:

            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            time = tds[1].get_text() or ''

            arrivaltime_ = time
            destination_ = tds[2].get_text() or ' '
            number = tds[3].get_text() or ' '
            carrier = tds[0].find("img").get("alt","") if tds[0].find("img") else "-"
            status = tds[4].get_text() or ' '
            flight = {
                FlightFields.arrivalTime: arrivaltime_,
                FlightFields.destination:destination_,
                FlightFields.carrier:carrier,
                FlightFields.number:number,
                FlightFields.status:status
            }
            flights_info.append(flight) 
        return flights_info