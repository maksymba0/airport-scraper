from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight, FlightFields
import cloudscraper as CloudScrapper

class BZG_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Bydgoszcz SA"
    airportCode_ = "BZG"

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
        for flight in flights:
    
            time = flight[FlightFields.arrivalTime].strip() 
            destination = flight[FlightFields.destination].strip() 
            number = flight[FlightFields.number].strip()
            gate = flight[FlightFields.gate].strip() 
            status = flight[FlightFields.status].strip() 
            carrier = flight[FlightFields.carrier].strip()
    
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
            number = flight[FlightFields.number].strip()
            gate = flight[FlightFields.gate].strip() 
            status = flight[FlightFields.status].strip() 
            carrier = flight[FlightFields.carrier].strip()
    
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
         
         
        print("downloading")
        scrapper = CloudScrapper.create_scraper(browser={
                            'browser':'chrome',
                            'platform':'windows',
                            'desktop':True
                        })
        data = scrapper.get(self.url_) 

        _data = data.text

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
                 FlightFields.arrivalTime: arrivaltime_,
                FlightFields.destination:destination_,
                FlightFields.number:number,
                FlightFields.carrier:carrier,
                FlightFields.gate:gate,
                FlightFields.status:status
            }
            flights_info.append(flight) 
        return flights_info  
    
    def getArrivals(self):

        print("downloading")

        scrapper = CloudScrapper.create_scraper()
        data = scrapper.get(self.url_) 
        
        #data = self.makeRequestHTML()  

        _data = data.text
        print(_data)
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
                FlightFields.arrivalTime: arrivaltime_,
                FlightFields.destination:destination_,
                FlightFields.number:number,
                FlightFields.carrier:carrier,
                FlightFields.gate:gate,
                FlightFields.status:status
            }
            flights_info.append(flight) 
        return flights_info  