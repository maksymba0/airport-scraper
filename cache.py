
import os
import json
from datetime import datetime, timedelta

CACHE_FILE = "flight_cache.json"
CACHE_DUR_MINUTES = 15

def load_cache():
    print("Loading from cache")
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE,"r", encoding="utf-8") as _file:
            data = json.load(_file)
        return data
    except (json.JSONDecodeError, IOError):
        return None
    
@DeprecationWarning
def save_cache(flights_data, airport_name=None):
    print("Saving to cache")
    data = {
        "timestamp" : datetime.now().isoformat(),
        "airport": airport_name,
        "flights":flights_data
    }
    with open(CACHE_FILE,"w", encoding="utf-8") as _file:
        json.dump(data, _file, indent=2, ensure_ascii=False)  
def save_cacheDB():
    data = {
             "timestamp" : datetime.now().isoformat()
         }
    with open(CACHE_FILE,"w", encoding="utf-8") as _file:
        json.dump(data, _file, indent=2, ensure_ascii=False)  

def is_valid_cache(cache_data):
    print("cache validation...")
    if not cache_data:
        return False
    timestamp_str = cache_data.get("timestamp")
    if not timestamp_str:
        return False
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        elapsed = datetime.now()- timestamp
        return elapsed.total_seconds() < (CACHE_DUR_MINUTES * 60)
    except ValueError:
        return False



def get_flights_dataDB(flights,airport_code = None):
     
    cache = load_cache()
    get_custom_airport = airport_code if (airport_code is not None and airport_code != 'all') else None 
    if not flights:
        print("[cache.py]: couldn't load cache")
        return []
    is_valid = is_valid_cache(cache)
    if not is_valid:
        print("[cache.py]: loaded invalid cache")
        return []
    if get_custom_airport:
        return [f for f in flights if f.get("code") == airport_code]
    return flights


@DeprecationWarning    
def get_flights_data(airport_code = None):
    cache = load_cache()
    get_custom_airport = airport_code if (airport_code is not None and airport_code != 'all') else None 
    if not cache:
        print("[cache.py]: couldn't load cache")
        return []
    is_valid = is_valid_cache(cache)
    if not is_valid:
        print("[cache.py]: loaded invalid cache")
        return []
    if get_custom_airport:
        data = cache.get("flights",[])
        return [f for f in data if f.get("code") == airport_code]
    return cache.get("flights",[])


