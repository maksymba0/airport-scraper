from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class BZG_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Bydgoszcz SA"
    airportCode_ = "BZG"

    def __init__(self, url):
        super().__init__(url)
        print(f"{self.airportName_} scrapper - init")
        super().printUrl()

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
    
            time = panel["arrivalTime"].strip() 
            destination = panel["destination"].strip() 
            number = panel["flightNum"].strip()
            gate = panel["gate"].strip() 
            status = panel["status"].strip() 
            carrier = panel["carrier"].strip()
    
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
            time = flight["arrivalTime"].strip() 
            destination = flight["destination"].strip() 
            number = flight["flightNum"].strip()
            gate = flight["gate"].strip() 
            status = flight["status"].strip() 
            carrier = flight["carrier"].strip()
    
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
    
        data = self.makeRequestHTML("https://poznanairport.pl/wp-json/api/v1/board/?page=1&phrase=&type=departures&day=0&timeFrom=00:00&timeTo=23:59&count=10&lang=pl") 
         
        with open("test.txt", "r", encoding="utf-8") as file_:
            if file_.read(1):
                print("reading")
                file_.seek(0)
                data = file_.read()
        if data == "":
            
            print("downloading")
            data = self.makeRequestHTML()  

        _data = data

        with open("test.txt","w",encoding="utf-8") as file:
            try: 
                file.write(data)
            except TypeError:
                file.write(data.text)

        data_ = JSON.loads(_data)
            

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in data_: 


            time = key['scheduledTime']

            arrivaltime_ = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%H:%M") or ""
            destination_ = key['airportNameEn'] or ' '
            number = key['flightNumber'] or ' '
            carrier = key['airlineName'] or ' '
            gate = key['gateNumbers'] or ' '
            status = key['statusEn'] or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "flightNum":number,
                "carrier":carrier,
                "gate":gate,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info  
    
    def getArrivals(self):

        data = ""
        with open("test.txt", "r", encoding="utf-8") as file_:
            if file_.read(1):
                print("reading")
                file_.seek(0)
                data = file_.read()
        if data == "":
            
            print("downloading")
            data = self.makeRequestHTML()  

        _data = data

        with open("test.txt","w",encoding="utf-8") as file:
            try: 
                file.write(data)
            except TypeError:
                file.write(data.text)

        data_ = JSON.loads(_data)
         

        print(f"Found {len(data_)} elements")

        flights_info = []
        for key in data_: 


            time = key['scheduledTime']

            arrivaltime_ = datetime.fromisoformat(time.replace("Z","+00:00")).strftime("%H:%M") or ""
            destination_ = key['airportNameEn'] or ' '
            number = key['flightNumber'] or ' '
            carrier = key['airlineName'] or ' '
            gate = key['gateNumbers'] or ' '
            status = key['statusEn'] or ' '
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "flightNum":number,
                "carrier":carrier,
                "gate":gate,
                "status":status
            }
            flights_info.append(flight) 
        return flights_info  