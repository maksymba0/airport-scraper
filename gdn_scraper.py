from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class GDN_Scraper(BaseScraper):

    airportName_ = "Gdansk Lech Walesa Airport"
    airportCode_ = "GDN"

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
                                <th style="padding: 5px;">Gate</th>
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
    
            raw_time = panel["dateTime"].strip()
            dtTime = datetime.fromisoformat(raw_time)
            time = dtTime.strftime("%H:%M")
            destination = panel["origin"].strip()
            carrier = panel["carrierName"].strip()
            number = panel["flight"].strip()
            status = panel["remarks"].strip() 
    
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
            raw_time = flight["dateTime"].strip()
            dtTime = datetime.fromisoformat(raw_time)
            time = dtTime.strftime("%H:%M")
            destination = flight["destination"].strip()
            carrier = flight["carrierName"].strip()
            #expectedTime = flight["expectedDateTime"].strip()
            number = flight["flight"].strip()
            status = flight["remarks"].strip()
            #bDomestic = flight["local"]
            gate = flight["gate"] or ""
    
            flight = Flight(time,destination,carrier,number,status) 
    
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
    
        data = self.makeRequestHTML("https://www.airport.gdansk.pl/loty/tablica-odlotow") 
        try:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        panel = _data.find('div', class_="table-schedule")
    
        rawData = panel['data-symfony--ux-react--react-props-value'] 
    
        PData = JSON.loads(rawData) 
        
        print("Keys found in data:", PData.keys()) 
        # ['arrivals', 'departures', 'locale', 'fetchedDate', 'securityWaitTime', 'isMainPage', 'ticketsLink']
    
        departures = PData.get('departures')
         
        if not departures:
            print("Couldn't get departures")
            return []
        
        departures_list = JSON.loads(departures)  

        return departures_list
    def getArrivals(self):

        data = self.makeRequestHTML() 
        try:
            _data = bs(data.text,"html.parser")
        except Exception as e:
            print(f"error: {e}")
            return []

        panel = _data.find('div', class_="table-schedule")
    
        rawData = panel['data-symfony--ux-react--react-props-value'] 
    
        PData = JSON.loads(rawData)

        with open("test.txt","w",encoding="utf-8") as file: 
            file.write(rawData) 
      
        print("Keys found in data:", PData.keys()) 
        # ['arrivals', 'departures', 'locale', 'fetchedDate', 'securityWaitTime', 'isMainPage', 'ticketsLink']
    
        arrivals = PData.get('arrivals')
        if not arrivals:
            print("Couldn't get arrivals")
            return []
        
        arrivals_list = JSON.loads(arrivals) 
                
        return arrivals_list