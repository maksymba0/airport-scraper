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
from services.flight_service import FlightService as FlightService

app = Flask(__name__)

@app.route("/api/get_flights")
def allFlights():
    force_refresh_ = request.args.get('refresh',False)
    airports_ = request.args.get('airports','all')
    return FlightService.get_flights(airports=airports_,force_refresh=force_refresh_)
        
 
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