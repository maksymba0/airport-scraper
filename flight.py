from dataclasses import dataclass
from typing import Optional

class FlightFields:
    flightNum= "flightNum",
    date = "date",
    time=  "time",
    destination=  "destination",
    origin=  "origin",
    status=  "status",
    carrier=  "carrier",
    gate=  "gate",
    terminal= "terminal",
    airport='airport',
    type=  "type",
    was_delayed= "was_delayed"
@dataclass
class Flight:

    flightNum: Optional[str] = None
    date: Optional[str] = None
    airport: Optional[str] = None
    time: Optional[str] = None
    destination: Optional[str] = None
    origin: Optional[str] = None
    status: Optional[str] = None
    carrier: Optional[str] = None
    gate: Optional[str] = None
    terminal: Optional[str] = None
    type: Optional[str] = None
    was_delayed: Optional[bool] = False

    def to_dict(self):
        return {
            "flightNum": self.flightNum,
            "date": self.date,
            "time": self.time,
            "airport": self.airport,
            "destination": self.destination,
            "origin": self.origin,
            "status": self.status,
            "carrier": self.carrier,
            "gate": self.gate,
            "terminal": self.terminal,
            "type": self.type,
            "was_delayed" : self.was_delayed
        }