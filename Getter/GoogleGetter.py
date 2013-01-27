import requests
import json

class GoogleGetter:
    
    def __init__(self):
        self.base_url = 'http://finance.google.com/finance/info?q='
    
    # @@@ add some error handling...
    def get_stock_value(self, symbol):
        r = requests.get(self.base_url + symbol)
        r.raise_for_status()
        lines = r.text.splitlines()
        json_data = json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
        return float(json_data["l"].replace(",", "")) / 100.0
        