from scrapers.basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields

class LUZ_Scraper(BaseScraper):

    airportName_ = "Port lotniczy lublin SA"
    airportCode_ = "LUZ"

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
        for flight in flights:
    
            time = flight[FlightFields.arrivalTime].strip() 
            destination = flight[FlightFields.destination].strip() 
            number = flight[FlightFields.number].strip() 
            status = flight[FlightFields.status].strip() 

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
            time = flight[FlightFields.arrivalTime].strip() 
            destination = flight[FlightFields.destination].strip() 
            number = flight[FlightFields.number].strip() 
            status = flight[FlightFields.status].strip()   
 
    
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

        tbody = data_.find("div",id="departures-table").find("div",role="table").find_all("div",recursive=False)[1]

        trs = tbody.find_all("div",recursive=False)

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("div",recursive=False)
            
            time = tds[0].get_text() or ''
            flight_ = Flight()
            flight_.time = time
            flight_.destination = tds[2].find("p").get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.status = tds[5].get_text().split() or ' '
            carrierText = tds[4].find("img").get("alt") if tds[4].find("img") else "-"
            flight_.carrier = "-"
            if carrierText == "LO":
            
                flight_.carrier = "LOT"
            elif carrierText == "W6":
                flight_.carrier = "WIZZ AIR"
            elif carrierText == "FR":
                flight_.carrier = "RYANAIR"
            elif carrierText == "E4":
                flight_.carrier ="ENTER AIR"
            else:
                flight_.carrier = carrierText
            
            flight = flight_.to_dict()
            
            flights_info.append(flight) 
        return flights_info   

    def getArrivals(self):

        data = self.makeRequestHTML() 
        
        _data = data.text
        
        
        data_ = bs(_data,"html.parser")

        tbody = data_.find("div",id="arrivals-table").find("div",role="table").find_all("div",recursive=False)[1]

        trs = tbody.find_all("div",recursive=False)

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in trs:

            tds = key.find_all("div",recursive=False)
            
            time = tds[0].get_text() or ''
            flight_ = Flight()

            flight_.time = time
            flight_.origin = tds[2].find("p").get_text() or ' '
            flight_.flightNum = tds[3].get_text() or ' '
            flight_.status = tds[5].get_text().split() or ' '
            carrierText = tds[4].find("img").get("alt") if tds[4].find("img") else "-";
            flight_.carrier = "-"
            if carrierText == "LO":
            
                flight_.carrier = "LOT"
            elif carrierText == "W6":
                flight_.carrier = "WIZZ AIR"
            elif carrierText == "FR":
                flight_.carrier = "RYANAIR"
            elif carrierText == "E4":
                flight_.carrier ="ENTER AIR"
            else:
                flight_.carrier = carrierText
            
            flight = flight_.to_dict()
            flights_info.append(flight) 
        return flights_info  