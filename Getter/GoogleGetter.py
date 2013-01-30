import urllib2, json, logging

class GoogleGetter:
    
    def __init__(self):
        self.base_url = 'http://www.google.co.uk/finance/info'
        self.logger = logging.getLogger("GoogleGetter")
    
    def get_stock_value(self, symbol):
        self.logger.info("Retrieving stock %s from Google" % symbol)
        # Get the raw json text
        lines = urllib2.urlopen(self.base_url, params={'q': symbol}).readlines()
        # Drop newline characters
        lines = map(lambda x: x.strip(), lines)
        # Remove unwanted lines and concatenate
        json_text = ''.join([x for x in lines if x not in ('// [', ']')])
        # Load as json
        json_data = json.loads(json_text)
        # Get the latest ("l") value
        value = float(json_data["l"].replace(",", "")) / 100.0
        self.logger.debug("Got value %.4f" % value) 
        return value