from Stocker.Data import *
from Stocker.Getter.GoogleGetter import GoogleGetter
import shelve, datetime

class Trader:

    def __init__(self):
        self.stocks = map(lambda x: x[0], FTSE_100)
        self.data = shelve.open("stocker_data")
        self.getter = GoogleGetter()
        
    def update_all_stocks(self):
        for stock in self.stocks:
            # Get existing data
            if self.data.has_key(stock):
                stock_data = self.data[stock]
            else:
                stock_data = StockData()
            
            # Add an entry for today
            stock_data.add_value(self.getter.get_stock(stock))
            
            # Save it back
            self.data[stock] = stock_data


class StockData:
    
    def __init__(self):
        self.history = {}
        self.purchases = []            
        
    def add_value(self, value, date=datetime.date.today()):
        self.history[date] = value