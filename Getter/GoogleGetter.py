import requests
import json

class GoogleGetter:
    
    def __init__(self):
        self.base_url = 'http://finance.google.com/finance/info?q='
    
    # @@@ add some error handling...
    def get_stock(self, symbol):
        url = self.base_url + symbol
        print url
        lines = requests.get(url).text.splitlines()
        print lines
        json_data = json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
        return float(json_data["l"].replace(",", ""))
        