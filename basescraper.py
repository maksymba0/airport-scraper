import requests
class BaseScraper:

    def __init__(self, url):
        self.url_ = url 

    def printUrl(self):
        print(self.url_)
        return self.url_

    def makeRequestHTML(self,arg):
        print(f"Attempting to request data at {arg}")
        if arg is None:
            arg = self.url
        try:
            # Mimic a standard Chrome browser header
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            result = requests.get(arg, headers=headers)
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
    