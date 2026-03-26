import requests

class NSEIndiaScraper:
    BASE_URL = "https://www.nseindia.com"

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.session.get(self.BASE_URL)  # create session

    def get_quote(self, symbol):
        url = f"{self.BASE_URL}/api/quote-equity?symbol={symbol}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        print(f"quote data ====> {response.json()}")
        return response.json()


def get_ltp(symbol):
    data = NSEIndiaScraper().get_quote(symbol)
    return data["priceInfo"]["lastPrice"]
