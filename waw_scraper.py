from basescraper import BaseScraper
import requests
from bs4 import BeautifulSoup as bs
import json as JSON
from datetime import datetime
from flight import Flight

class WAW_Scraper(BaseScraper):

    airportName_ = "Warsaw Chopin Airport"
    airportCode_ = "WAW"

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
            carrier = flight["carrierName"].strip() 
            number = flight["flightNum"].strip()
            status = flight["status"].strip() 
            gate = flight["gate"] or "" 
    
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

        flights = []

        for flight in departures_list:
            raw_time = flight["arrivalTime"].strip()
            dtTime = datetime.fromisoformat(raw_time)
            time = dtTime.strftime("%H:%M")
            destination = flight["destination"].strip()
            carrier = flight["carrierName"].strip() 
            number = flight["flightNum"].strip()
            status = flight["status"].strip() 
            gate = flight["gate"] or ""

            _flight = {
                "arrivalTime": time,
                "destination":destination,
                "flightNum":carrier + " " +number, 
                "status":status
                }
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
            data = self.makeRequestHTML() 
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

        flights_list = _data.find('ul', class_="flights-list")

        flights = flights_list.find_all("li",class_="arrivals-departures-tables") 

        print(f"Found {len(flights)} elements")

        flights_info = []
        for li in flights[1:]: 

            arrivaltime_ = t.get_text(strip=True) if (t := li.select_one(".column-time.arrivals-col")) else ""
            destination_ = t.get_text(strip=True) if (t := li.select_one(".column-origin-destination")) else ""
            number = t.get_text(strip=True) if (t := li.select_one(".column-flight-no")) else ""
            carrier = t.get("alt","") if (t := li.select_one(".column-airline img")) else ""
            gate = t.get_text(strip=True) if (t := li.select_one(".column-gate")) else ""
            status = t.get_text(strip=True) if (t := li.select_one(".column-status")) else ""
            flight = {
                "arrivalTime": arrivaltime_,
                "destination":destination_,
                "flightNum":number,
                "carrier":carrier,
                "gate":gate,
                "status":status
            }
            flights_info.append(flight)
        #flights_info_text = " \n".join(flights_info)
        #print(flights_info_text)
        print(flights_info)
        return flights_info  