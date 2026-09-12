def get_airline_name(flight_number: str) -> str:
    carrier = flight_number.strip().replace(" ", "").upper()

    airline_codes = {
        # Poland
        "LO": "LOT",
        "E4": "ENTER AIR",

        # Ireland / UK
        "FR": "RYANAIR",
        "RR": "RYANAIR",
        "BA": "BRITISH AIRWAYS",
        "U2": "EASYJET",
        "LS": "JET2",
        "BY": "TUI AIRWAYS",
        "TOM": "TUI UK & IRELAND",

        # Hungary / Central Europe
        "W6": "WIZZ AIR",
        "5W": "WIZZ AIR ABU DHABI",
        "W4": "WIZZ AIR MALTA",
        "W9": "WIZZ AIR UK",
        "OS": "AUSTRIAN AIRLINES",
        "OK": "CZECH AIRLINES",
        "QS": "SMARTWINGS",
        "EW": "EUROWINGS",

        # Germany / Switzerland
        "LH": "LUFTHANSA",
        "LX": "SWISS",
        "SN": "BRUSSELS AIRLINES",
        "DE ": "CONDOR",

        # France / Netherlands
        "AF": "AIR FRANCE",
        "KL": "KLM",
        "TO": "TRANSAVIA FRANCE",
        "HV": "TRANSAVIA",
        "VY": "VUELING",

        # Spain / Portugal
        "IB": "IBERIA",
        "UX": "AIR EUROPA",
        "TP": "TAP AIR PORTUGAL",
        "FR": "RYANAIR",
        "YW":"AIR NOSTRUM",

        # Italy
        "AZ": "ITA AIRWAYS",
        "XZ": "AEROITALIA",
        "EN": "AIR DOLOMITI",

        # Scandinavia
        "SK": "SAS",
        "DY": "NORWEGIAN",
        "D8": "NORWEGIAN",
        "WF": "WIDEROE",
        "AY": "FINNAIR",
        "FI": "ICELANDAIR",

        # Greece
        "A3": "AEGEAN AIRLINES",
        "GQ": "SKY EXPRESS",
        "OA": "OLYMPIC AIR",

        # Turkey
        "TK": "TURKISH AIRLINES",
        "PC": "PEGASUS AIRLINES",
        "XQ": "SUNEXPRESS",
        "XC": "CORONDON AIRLINES",

        # Middle East
        "EK": "EMIRATES",
        "QR": "QATAR AIRWAYS",
        "EY": "ETIHAD AIRWAYS",
        "FZ": "FLYDUBAI",
        "RJ": "ROYAL JORDANIAN",
        "SV": "SAUDI ARABIAN AIRLINES",
        "LY": "EL AL",

        # North America
        "AA": "AMERICAN AIRLINES",
        "UA": "UNITED AIRLINES",
        "DL": "DELTA AIR LINES",
        "AC": "AIR CANADA",
        "WS": "WESTJET",
        "B6": "JETBLUE",
        "WN": "SOUTHWEST AIRLINES",

        # Asia
        "SQ": "SINGAPORE AIRLINES",
        "CX": "CATHAY PACIFIC",
        "JL": "JAPAN AIRLINES",
        "NH": "ALL NIPPON AIRWAYS",
        "KE": "KOREAN AIR",
        "OZ": "ASIANA AIRLINES",
        "CA": "AIR CHINA",
        "MU": "CHINA EASTERN AIRLINES",
        "CZ": "CHINA SOUTHERN AIRLINES",
        "AI": "AIR INDIA",

        # Australia / New Zealand
        "QF": "QANTAS",
        "JQ": "JETSTAR",
        "NZ": "AIR NEW ZEALAND",

        # Africa
        "MS": "EGYPTAIR",
        "ET": "ETHIOPIAN AIRLINES",
        "AT": "ROYAL AIR MAROC",
        "SA": "SOUTH AFRICAN AIRWAYS",
    }

    # Check longest codes first
    for code in sorted(airline_codes, key=len, reverse=True):
        if carrier.startswith(code):
            return airline_codes[code]

    # Unknown airline
    return '-'