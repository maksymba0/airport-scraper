class FlightFields:
    arrivalTime = "arrivalTime"
    destination = "destination"
    number = "flightNum"
    status = "status"
    carrier = "carrier"
    gate = "gate"

class Flight:
    time_ = ""
    route_ = ""
    carrier_ = ""
    number_ = ""
    status_ = "" 
    def __init__(self, time,route,carrier,number,status):
        self.time_ = time
        self.route_ = route
        self.carrier_ = carrier
        self.number_ = number
        self.status_ = status
    def __repr__(self):
        return f"{self.time_} - {self.route_} - {self.carrier_} - {self.number_} - {self.status_}"
    def dump():
        print("Dumping")
    def asString(self):
        return f"{self.time_} - {self.route_} - {self.carrier_} - {self.number_} - {self.status_}"

