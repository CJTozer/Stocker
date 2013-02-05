import requests, json, logging

class GoogleGetter:
    
    def __init__(self):
        self.base_url = 'http://www.google.co.uk/finance/info'
        self.logger = logging.getLogger("GoogleGetter")
    
    def get_stock_value(self, symbol):
        self.logger.info("Retrieving stock %s from Google" % symbol)
        # Give it 3 goes...
        for ii in range(3):
            r = requests.get(self.base_url, params={'q': "LON:%s" % symbol})
            self.logger.info("Response: %d" % r.status_code)
            if r.status_code == 200:
                break
            print "Failed to fetch stock %s %d time(s)" % (symbol, ii + 1)            
        r.raise_for_status()
        lines = r.text.splitlines()
        json_data = json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
        value = float(json_data["l"].replace(",", "")) / 100.0
        self.logger.debug("Got value %.4f" % value) 
        return value