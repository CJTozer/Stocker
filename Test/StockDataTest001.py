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
    
    def test_get_historical_value(self):
        """ Test that we ignore weekends for historical values """
        # date[0] is a Tuesday, so date[4] and date[5] are weekends
        stock_data = StockData()
        dates = map(lambda x: datetime.date(2013, 1, x), range(1, 10))
        for ii in range(9):
            stock_data.add_history_value(ii, dates[ii])
        
        # First dates back from 8
        self.assertEquals(stock_data.get_historical_value(0, start_date=dates[8]), 8)
        self.assertEquals(stock_data.get_historical_value(1, start_date=dates[8]), 7)
        self.assertEquals(stock_data.get_historical_value(2, start_date=dates[8]), 6)
        self.assertEquals(stock_data.get_historical_value(3, start_date=dates[8]), 3)
        self.assertEquals(stock_data.get_historical_value(4, start_date=dates[8]), 2)
        self.assertEquals(stock_data.get_historical_value(5, start_date=dates[8]), 1)
        self.assertEquals(stock_data.get_historical_value(6, start_date=dates[8]), 0)
        self.assertEquals(stock_data.get_historical_value(7, start_date=dates[8]), -1)
        
        # Then back from 7
        self.assertEquals(stock_data.get_historical_value(0, start_date=dates[7]), 7)
        self.assertEquals(stock_data.get_historical_value(1, start_date=dates[7]), 6)
        self.assertEquals(stock_data.get_historical_value(2, start_date=dates[7]), 3)
        self.assertEquals(stock_data.get_historical_value(3, start_date=dates[7]), 2)
        self.assertEquals(stock_data.get_historical_value(4, start_date=dates[7]), 1)
        self.assertEquals(stock_data.get_historical_value(5, start_date=dates[7]), 0)
        self.assertEquals(stock_data.get_historical_value(6, start_date=dates[7]), -1)
        
        # From 6
        self.assertEquals(stock_data.get_historical_value(0, start_date=dates[6]), 6)
        self.assertEquals(stock_data.get_historical_value(1, start_date=dates[6]), 3)
        self.assertEquals(stock_data.get_historical_value(2, start_date=dates[6]), 2)
        self.assertEquals(stock_data.get_historical_value(3, start_date=dates[6]), 1)
        self.assertEquals(stock_data.get_historical_value(4, start_date=dates[6]), 0)
        self.assertEquals(stock_data.get_historical_value(5, start_date=dates[6]), -1)
        
        # From 5 - getting there...
        self.assertEquals(stock_data.get_historical_value(0, start_date=dates[5]), 3)
        self.assertEquals(stock_data.get_historical_value(1, start_date=dates[5]), 2)
        self.assertEquals(stock_data.get_historical_value(2, start_date=dates[5]), 1)
        self.assertEquals(stock_data.get_historical_value(3, start_date=dates[5]), 0)
        self.assertEquals(stock_data.get_historical_value(4, start_date=dates[5]), -1)
        
        # From 4 - last one
        self.assertEquals(stock_data.get_historical_value(0, start_date=dates[4]), 3)
        self.assertEquals(stock_data.get_historical_value(1, start_date=dates[4]), 2)
        self.assertEquals(stock_data.get_historical_value(2, start_date=dates[4]), 1)
        self.assertEquals(stock_data.get_historical_value(3, start_date=dates[4]), 0)
        self.assertEquals(stock_data.get_historical_value(4, start_date=dates[4]), -1)
    
    ##
    ## Utilities
    ##
    def get_today(self, days_to_add):
        return datetime.date.today() + datetime.timedelta(days=days_to_add)
        

if __name__ == '__main__':
    unittest.main()