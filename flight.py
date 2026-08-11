from dataclasses import dataclass
from typing import Optional

class FlightFields:
    flightNum= "flightNum",
    time=  "time",
    destination=  "destination",
    origin=  "origin",
    status=  "status",
    carrier=  "carrier",
    gate=  "gate",
    terminal= "terminal",
    type=  "type"
@dataclass
class Flight:

    flightNum: Optional[str] = None
    time: Optional[str] = None
    destination: Optional[str] = None
    origin: Optional[str] = None
    status: Optional[str] = None
    carrier: Optional[str] = None
    gate: Optional[str] = None
    terminal: Optional[str] = None
    type: Optional[str] = None

    def to_dict(self):
        return {
            "flightNum": self.flightNum,
            "time": self.time,
            "destination": self.destination,
            "origin": self.origin,
            "status": self.status,
            "carrier": self.carrier,
            "gate": self.gate,
            "terminal": self.terminal,
            "type": self.type
        }