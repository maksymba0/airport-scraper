from flask import Flask, jsonify, render_template, request
import home as _home
from flight import Flight, FlightFields
 

#import json as JSON
from datetime import datetime 

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