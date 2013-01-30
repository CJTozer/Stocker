import unittest, logging, datetime
from Stocker.Trader import StockData
from Stocker.Rules import Transaction

logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(name)-16s%(message)s',
                    filename='Test.log',
                    filemode = 'w',
                    level=logging.DEBUG)
logger = logging.getLogger("StockDataTest001")

class StockDataTest001(unittest.TestCase):
    """ Basic tests of StockData. """

    def test_new_stock(self):      
        """ Create a new StockData """
        stock_data = StockData()
        self.assertNotEqual(stock_data, None)
        self.assertEqual(stock_data.holding, 0)
        self.assertEqual(stock_data.last_value, 0.0)
        self.assertEqual(stock_data.transactions, [])
        self.assertEqual(stock_data.history, {})
        
    def test_add_history(self):
        """ Add some historical data and get it back """
        stock_data = StockData()
        stock_data.add_history_value(1.0, self.get_today(0))
        stock_data.add_history_value(2.0, self.get_today(-1))
        self.assertEqual(stock_data.get_historical_value(0), 1.0)
        self.assertEqual(stock_data.get_historical_value(1), 2.0)
        self.assertEqual(stock_data.get_historical_value(2), -1.0)

    def test_buy(self):
        """ Test purchases """
        stock_data = StockData()
        t1 = Transaction(2, 3.0)
        cost = stock_data.apply_transaction(t1)
        self.assertEqual(cost, 6.0)
        self.assertEqual(stock_data.holding, 2)
        self.assertEqual(stock_data.transactions, [t1])

    def test_sell(self):
        """ Test sales """
        stock_data = StockData()
        t1 = Transaction(5, 2.5)
        cost = stock_data.apply_transaction(t1)
        self.assertEqual(cost, 12.5)
        t2 = Transaction(-2, 3.2)
        cost = stock_data.apply_transaction(t2)
        self.assertEqual(cost, -6.4)
        self.assertEqual(stock_data.holding, 3)
        self.assertEqual(stock_data.transactions, [t1, t2])
        
    def test_sorted_holdings_value(self):
        """ Test get_sorted_holdings_value """
        stock_data = StockData()
        ts = [Transaction(4, 2.5, date=self.get_today(-4)),  # 2.5, 2.5, 2.5, 2.5
              Transaction(-2, 3.2, date=self.get_today(-3)), # 2.5, 2.5 
              Transaction(1, 3.0, date=self.get_today(-2)),  # 2.5, 2.5, 3.0
              Transaction(2, 2.6, date=self.get_today(-1)),  # 2.5, 2.5, 2.6, 2.6, 3.0
              Transaction(-3, 2.9, date=self.get_today(0))]  # 2.6, 3.0
        for t in ts:
            stock_data.apply_transaction(t)
            
        # Total holding should be 5.6
        self.assertEqual(stock_data.holding, 2)
        self.assertEqual(stock_data.transactions, ts)
        self.assertEqual(stock_data.sorted_holdings_value(), 5.6)
        
    ##
    ## Utilities
    ##
    def get_today(self, days_to_add):
        return datetime.date.today() + datetime.timedelta(days=days_to_add)
        

if __name__ == '__main__':
    unittest.main()