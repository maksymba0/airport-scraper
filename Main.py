from flask import Flask, jsonify
import home as _home
from flight import Flight
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

#import json as JSON
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home(): 

    Gdansk = gdn_scraper.GDN_Scraper("https://www.airport.gdansk.pl/loty/tablica-przylotow")
    WarsawC = waw_scraper.WAW_Scraper("https://lotnisko-chopina.pl/en/arrivals-and-departures/")
    Krakow = krk_scraper.KRK_Scraper("https://krakowairport.pl/pl/pasazer/loty/polaczenia/przyloty")
    Wroclaw = wro_scraper.WRO_Scraper("https://airport.wroclaw.pl/wp-admin/admin-ajax.php?lang=pl&action=maly_rozklad_lotow")
    Szczecin = szz_scraper.SZZ_Scraper("https://airport.com.pl/loty/tablica-przylotow-odlotow/")
    Bydgoszcz = bzg_scraper.BZG_Scraper("https://plb.pl/wp-admin/admin-ajax.php?action=get_flights_arrivals")
    Poznan = poz_scraper.POZ_Scraper("https://poznanairport.pl/wp-json/api/v1/board/?page=1&phrase=&type=arrivals&day=0&timeFrom=00:00&timeTo=23:59&count=10&lang=pl")
    Katowice = ktw_scraper.KTW_Scraper("None")
    Lodz = lcj_scraper.LCJ_Scraper("https://www.lodz-airport.pl/pl")
    Rzeszow = rze_scraper.RZE_Scraper("https://www.rzeszowairport.pl/pl/pasazer/loty")
    Radom = rdo_scraper.RDO_Scraper("https://www.lotniskowarszawa-radom.pl/api/search-flight")
    Olsztyn = szy_scraper.SZY_Scraper("https://mazuryairport.pl/")
    

    result = Olsztyn.getArrivalsTable()
    departures = Olsztyn.getDeparturesAsTable()
    #Bydgoszcz.getArrivalsTable()
    #departures = Gdansk.getDeparturesAsTable()
    #arrivals = Gdansk.getArrivalsTable()

    #f"<h>Airport data: </h> <p>{departures}</p> <p>{arrivals}</p>"
    output = f"<h>Airport data: </h> <p>{result}</p> <p>{departures}</p>"

    return output 
@app.route("/api/ping")
def ping():
    return jsonify({"status":"ok","message":"Flask is alive"})

def main():
    print("Starting")
    app.run(debug=True)
print("Hello world")
if __name__ == '__main__':
    main()