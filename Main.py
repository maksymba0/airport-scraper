from flask import Flask, jsonify, render_template
import home as _home
from flight import Flight, FlightFields

import gdn_scraper 
import waw_scraper
import krk_scraper
import wro_scraper
import szz_scraper
import bzg_scraper
import poz_scraper
import ktw_scraper
import lcj_scraper
import rze_scraper
import rdo_scraper
import szy_scraper
import luz_scraper

#import json as JSON
from datetime import datetime
app = Flask(__name__)

@app.route("/api/all-flights")
def allFlights():

    airports = {
            "GDN" : gdn_scraper.GDN_Scraper("https://www.airport.gdansk.pl/loty/tablica-przylotow"),
            "SZZ" : szz_scraper.SZZ_Scraper("https://airport.com.pl/loty/tablica-przylotow-odlotow/"),
            "WRO" : wro_scraper.WRO_Scraper("https://airport.wroclaw.pl/wp-admin/admin-ajax.php?lang=pl&action=maly_rozklad_lotow"),
            "KRK" : krk_scraper.KRK_Scraper("https://krakowairport.pl/pl/pasazer/loty/polaczenia/przyloty"),
            #"POZ" : poz_scraper.POZ_Scraper("https://poznanairport.pl/wp-json/api/v1/board/?page=1&phrase=&type=arrivals&day=0&timeFrom=00:00&timeTo=23:59&count=10&lang=pl"),
            "WAW" : waw_scraper.WAW_Scraper("https://lotnisko-chopina.pl/en/arrivals-and-departures/"),
            "BZG" : bzg_scraper.BZG_Scraper("https://plb.pl/wp-admin/admin-ajax.php?action=get_flights_arrivals"),
            "KTW" : ktw_scraper.KTW_Scraper("None"), #its okay, let it be None
            "LCJ" : lcj_scraper.LCJ_Scraper("https://www.lodz-airport.pl/pl"),
            "RZE" : rze_scraper.RZE_Scraper("https://www.rzeszowairport.pl/pl/pasazer/loty"),
            "RDO" : rdo_scraper.RDO_Scraper("https://www.lotniskowarszawa-radom.pl/api/search-flight"),
            "SZY" : szy_scraper.SZY_Scraper("https://mazuryairport.pl/"),
            "LUZ" : luz_scraper.LUZ_Scraper("https://www.airport.lublin.pl/")
    }
    all_flights = []

    for code, scraper in airports.items():
        arrivals = scraper.getArrivals()
        departures = scraper.getDepartures()

        for flight in arrivals:
            flight["code"] = code
            flight["type"] = "arrival"
        for flight in departures:
            flight["code"] = code
            flight["type"] = "departures"   
        all_flights.extend(arrivals)
        all_flights.extend(departures)

    return jsonify(
        {
        "count":len(all_flights),
        "flights":all_flights,
        "last_updated":datetime.now().isoformat()
        })
        



    return ""
@app.route("/")
def home(): 

    return render_template("dashboard.html")

@app.route("/api/ping")
def ping():
    return jsonify({"status":"ok","message":"Flask is alive"})

def main():
    print("Starting")
    app.run(debug=True)
print("Hello world")
if __name__ == '__main__':
    main()