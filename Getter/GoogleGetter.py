import requests, json, logging

class GoogleGetter:
    
    def __init__(self):
        self.base_url = 'http://74.125.132.94/finance/info'
        self.logger = logging.getLogger("GoogleGetter")
    
    def get_stock_value(self, symbol):
        self.logger.info("Retrieving stock %s from Google" % symbol)
        r = requests.get(self.base_url, params={'q': symbol})
        print r.headers
        self.logger.info(r.headers)
        r.raise_for_status()
        lines = r.text.splitlines()
        json_data = json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
        value = float(json_data["l"].replace(",", "")) / 100.0
        self.logger.debug("Got value %.4f" % value) 
        return value