import logging

class TestGetter:
    
    def __init__(self):
        # Start off with no data...
        self.data = {}
        self.logger = logging.getLogger("Trader")
    
    def get_stock_value(self, symbol):
        self.logger.info("Retrieving stock %s from TestGetter" % symbol)
        value = self.data[symbol]
        self.logger.debug("Returning value %.4f" % value)
        return value