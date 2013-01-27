from Data import FTSE_100   
from Getter.GoogleGetter import GoogleGetter
import shelve, datetime

class Trader:

    def __init__(self):
        self.stocks = map(lambda x: x[0], FTSE_100)
        self.data = shelve.open("stocker_data")
        self.getter = GoogleGetter()
        if self.data.has_key('cash'):
            self.cash = self.data['cash']
        else:
            self.cash = 1000.0
        
    def update_all_stocks(self):
        for stock in self.stocks:
            self.update_stock(stock)
            
    def update_stock(self, stock):
        # Get existing data
        stock_data = self.get_stock_data(stock)
            
        # Add an entry for today
        stock_data.add_history_value(self.getter.get_stock_value(stock))
            
        # Save it back
        self.save_stock_data(stock, stock_data)
            
    def total_stock_value(self):
        total = 0.0
        for stock in self.stocks:
            stock_data = self.get_stock_data(stock)
            total += stock_data.last_value * stock_data.holding
        return total 
            
    def get_stock_data(self, stock):
        print "Getting stock '%s'" % stock
        if self.data.has_key(stock):
            stock_data = self.data[stock]
        else:
            stock_data = StockData()
        return stock_data

    def save_stock_data(self, stock, stock_data):
        self.data[stock] = stock_data

    def __str__(self):
        return "Trader:\n" \
               "Cash: %.2f\n" \
               "Stocks: %.2f" % (self.cash, self.total_stock_value())

class StockData:

    def __init__(self):
        self.history = {}
        self.purchases = []
        self.holding = 0
        self.last_value = 0

    def buy(self, purchase):
        self.holding += purchase.quantity
        self.purchases.append(purchase)

    def add_history_value(self, value, date=datetime.date.today()):
        self.history[date] = value
        self.last_value = value 


class Purchase:
    
    def __init__(self, date, quantity, price):
        self.date = date
        self.quantity = quantity
        self.price = price
        
    def cost(self):
        return self.price * self.quantity        