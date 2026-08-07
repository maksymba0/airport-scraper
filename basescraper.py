import requests
class BaseScraper:

    def __init__(self, url):
        self.url_ = url 

    def printUrl(self):
        print(self.url_)
        return self.url_

    def makeRequestHTML(self,arg, headers=None, method=None, json=None): 
        header_ = headers if headers is not None else {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        method_ = method or None
        json_ = json if json is not None else ""


        print(f"Attempting to request data at {arg}")
        if arg is None:
            arg = self.url
        try:
            # Mimic a standard Chrome browser header 
            if method_ is None:
                print("sent get request")
                result = requests.get(arg, headers=header_)
            else:
                print("sent post request")
                result = requests.post(arg, headers=header_, json=json_)    

        except Exception as e:
            error = (f"Failed to send request to {arg}: {e}")
            print(error)
            return None
        else:
            if result.status_code == 200:
                print(f"request data - Success ({result.status_code})")
            else:
                print(f"request data - Failure ({result.status_code})")
            return result
    