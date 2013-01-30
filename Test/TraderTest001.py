import unittest, logging, datetime
from Stocker.Trader import Trader
from Stocker.Test.TestGetter import TestGetter

logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(name)-16s%(message)s',
                    filename='Test.log',
                    filemode = 'w',
                    level=logging.DEBUG)
logger = logging.getLogger("TraderTest001")

class TraderTest001(unittest.TestCase):
    """ Basic tests of Trader acting on stocks. """

    def setUp(self):
        """ Create a trader and dummy up the data """
        self.trader = Trader(name="test")
        self.trader.data = {}
        
        # Create a fake Getter
        self.getter = TestGetter()
        
        # Give the Trader the fake Getter
        self.trader.getter = self.getter

    def test_new_stock(self):      
        """ Get a stock data that doesn't exist yet """
        self.check_stock_data("TEST1")

    def test_update_stock(self):
        """ Give the getter a value, and update the stock """
        self.getter.data["TEST1"] = 123.456
        self.trader.update_stock("TEST1")
        self.check_stock_data("TEST1", last_value=123.456, history={datetime.date.today() : 123.456})
        
    def test_update_stock2(self):
        """ Update a stock twice """
        history={}
        self.getter.data["TEST1"] = 123.456
        self.trader.update_stock("TEST1")
        history[datetime.date.today()] = 123.456
        self.getter.data["TEST1"] = 987.654
        self.trader.update_stock("TEST1", date=(datetime.date.today() - datetime.timedelta(days=1)))
        history[datetime.date.today() - datetime.timedelta(days=1)] = 987.654
        self.check_stock_data("TEST1", last_value=987.654, history=history)

    ##
    ## Utilities
    ##
    def check_stock_data(self, symbol, holding=0, last_value=0.0, transactions=[], history={}):
        stock_data = self.trader.get_stock_data("TEST1")
        self.assertNotEqual(stock_data, None)
        self.assertEqual(stock_data.holding, holding)
        self.assertEqual(stock_data.last_value, last_value)
        self.assertEqual(stock_data.transactions, transactions)
        self.assertEqual(stock_data.history, history)

if __name__ == '__main__':
    unittest.main()