from datetime import datetime
from typing import Optional
import sys
import os
from flask import Flask, jsonify, render_template, request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flight import Flight, FlightFields
from cache import load_cache, save_cache, is_valid_cache

from scrapers import bzg_scraper,gdn_scraper,krk_scraper,ktw_scraper,lcj_scraper,luz_scraper,poz_scraper,rdo_scraper,rze_scraper,szy_scraper,szz_scraper,waw_scraper,wro_scraper 

class FlightService:

    @staticmethod
    def get_all_flights(force_refresh: bool = False) -> dict:

        b_force = False if force_refresh is None else force_refresh 

        if not b_force:
            cache_ = load_cache()
            if cache_ and is_valid_cache(cache_):
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
                "SZZ" : szz_scraper.SZZ_Scraper("https://airport.com.pl/loty/tablica-przylotow-odlotow/"),
                "WRO" : wro_scraper.WRO_Scraper("https://airport.wroclaw.pl/wp-admin/admin-ajax.php?lang=pl&action=maly_rozklad_lotow"),
                "KRK" : krk_scraper.KRK_Scraper("https://krakowairport.pl/pl/pasazer/loty/polaczenia/przyloty"),
                "GDN" : gdn_scraper.GDN_Scraper("https://www.airport.gdansk.pl/loty/tablica-przylotow"),
                "KRK" : krk_scraper.KRK_Scraper("https://krakowairport.pl/pl/pasazer/loty/polaczenia/przyloty"),
                "POZ" : poz_scraper.POZ_Scraper("https://poznanairport.pl/wp-json/api/v1/board/?page=1&phrase=&type=arrivals&day=0&timeFrom=00:00&timeTo=23:59&lang=pl"),
                "WAW" : waw_scraper.WAW_Scraper("https://lotnisko-chopina.pl/en/arrivals-and-departures/"),
                #"BZG" : bzg_scraper.BZG_Scraper("https://plb.pl/wp-admin/admin-ajax.php?action=get_flights_arrivals"), #Disabled BZG temporarily due to clouidfare issues
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
                flight["type"] = "departure"   
            all_flights.extend(arrivals)
            all_flights.extend(departures) 

        save_cache(all_flights)
        return jsonify(
            {
            "cached":False,
            "flights":all_flights,
            "last_updated":datetime.now().isoformat()
            }) 