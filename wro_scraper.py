from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight
import cloudscraper as CloudScrapper



class WRO_Scraper(BaseScraper):

    airportName_ = "Port Lotniczy Wrocław SA"
    airportCode_ = "WRO"

    def __init__(self, url):
        super().__init__(url)
        print(f"{self.airportName_} scraper - init")
        super().printUrl()

    def makeRequestHTML(self,url=None):
  
        if url is None:
            url = self.url_

        result = super().makeRequestHTML(url) 

        return result


    def getArrivalsTableHeader(self):
        table_header = f"""
                <h>Arrivals:</h>
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
                <h>Departures:</h>
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
        for a in flights:
            print(a)
        print(flights)

        table_header = self.getArrivalsTableHeader()
    
        flights_text = []
        for panel in flights: 
            time = panel["arrivalTime"].strip() 
            destination = panel["destination"].strip() 
            number = panel["flightNum"].strip() 
            status = panel["status"].strip()  
    
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
        print(content)
    
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
        data = ""
        with open("test.txt", "r", encoding="utf-8") as file_:
            if file_.read(1):
                print("reading")
                file_.seek(0)
                data = file_.read()
        if data == "":
            
            print("downloading")
            scrapper = CloudScrapper.create_scraper(browser={
                'browser':'chrome',
                'platform':'windows',
                'desktop':True
            })
            data = scrapper.get(self.url_) 
        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        with open("test.txt","w",encoding="utf-8") as file:
            try: 
                file.write(data)
            except TypeError:
                file.write(data.text)



        flightsTable = _data.find('div', id="departures")

        flightsBody = flightsTable.find("table", class_="flight-table",recursive=False).find("tbody")

        trs = flightsBody.find_all("tr")


        flights = []
        
        for tr in trs:
            className = tr.get("class", []) # Safely get class list
            if "flight-info-popup-row" in className:
                continue   
            tds = tr.find_all("td")
            flightTime = tds[0].get_text(strip=True)
            airport = tds[1].find_all("div")[0].get_text(strip=True)
            flight_no = tds[2].get_text(strip=True)
            status = tds[3].get_text(strip=True)
            flight = {
                "arrivalTime": flightTime,
                "destination":airport,
                "flightNum":flight_no, 
                "status":status
            }
            flights.append(flight)

        print(f"Found {len(trs)} elements")
        return flights 
    def getArrivals(self):

        data = ""
        with open("test.txt", "r", encoding="utf-8") as file_:
            if file_.read(1):
                print("reading")
                file_.seek(0)
                data = file_.read()
        if data == "":
            
            print("downloading")
            scrapper = CloudScrapper.create_scraper(browser={
                'browser':'chrome',
                'platform':'windows',
                'desktop':True
            })
            data = scrapper.get(self.url_) 
        try:
            try:
                _data = bs(data,"html.parser")
            except Exception:
                _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        with open("test.txt","w",encoding="utf-8") as file:
            try: 
                file.write(data)
            except TypeError:
                file.write(data.text)



        flightsTable = _data.find('div', id="arrivals")

        flightsBody = flightsTable.find("table", class_="flight-table",recursive=False).find("tbody")

        trs = flightsBody.find_all("tr")

    
        flights = []
        
        for tr in trs:
            className = tr.get("class", []) # Safely get class list
            if "flight-info-popup-row" in className:
                continue   
            tds = tr.find_all("td")
            flightTime = tds[0].get_text(strip=True)
            airport = tds[1].find_all("div")[0].get_text(strip=True)
            flight_no = tds[2].get_text(strip=True)
            status = tds[3].get_text(strip=True)
            flight = {
                "arrivalTime": flightTime,
                "destination":airport,
                "flightNum":flight_no, 
                "status":status
            }
            flights.append(flight)
 
        print(f"Found {len(flights)} elements")
        return flights 