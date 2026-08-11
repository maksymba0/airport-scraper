from flask import Flask, jsonify, render_template, request
import home as _home
from flight import Flight, FlightFields

import scrapers.gdn_scraper as gdn_scraper 
import scrapers.waw_scraper as waw_scraper
import scrapers.krk_scraper as krk_scraper
import scrapers.wro_scraper as wro_scraper
import scrapers.szz_scraper as szz_scraper
import scrapers.bzg_scraper as bzg_scraper
import scrapers.poz_scraper as poz_scraper
import scrapers.ktw_scraper as ktw_scraper
import scrapers.lcj_scraper as lcj_scraper
import scrapers.rze_scraper as rze_scraper
import scrapers.rdo_scraper as rdo_scraper
import scrapers.szy_scraper as szy_scraper
import scrapers.luz_scraper as luz_scraper

#import json as JSON
from datetime import datetime
import cache
import requests

app = Flask(__name__)

@app.route("/api/all-flights")
def allFlights():

    bForce = request.args.get('refresh', 'false') == 'true'

   
    if not bForce:
        cache_ = cache.load_cache()
        if cache and cache.is_valid_cache(cache_):
            print("loading from cache")
            return jsonify(
                    {
                    "cached":True,
                    "flights":cache_["flights"],
                    "last_updated":cache_["timestamp"]
                    })
        else:
            print("cache expired or empty. building new data")
    else:
        print("Force refresh data. Building")


    airports = {
            "GDN" : gdn_scraper.GDN_Scraper("https://www.airport.gdansk.pl/loty/tablica-przylotow"),
            "KRK" : krk_scraper.KRK_Scraper("https://krakowairport.pl/pl/pasazer/loty/polaczenia/przyloty"),
            
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
            flight["type"] = "departure"   
        all_flights.extend(arrivals)
        all_flights.extend(departures)

    cache.save_cache(all_flights)

    return jsonify(
        {
        "cached":False,
        "flights":all_flights,
        "last_updated":datetime.now().isoformat()
        }) 
        
 
@app.route("/")
def home(): 

    return render_template("dashboard.html")

@app.route("/api/ping")
def ping():
    return jsonify({"status":"ok","message":"Flask is alive"})

def main():
    print("Starting")
    app.run(host='0.0.0.0',port=5555,debug=True)

print("Hello world")
if __name__ == '__main__':
    main()