from Data import FTSE_100   
from Getter.GoogleGetter import GoogleGetter
import shelve, datetime, logging

class Trader:

    def __init__(self, name="default", rules=[]):
        self.logger = logging.getLogger("Trader")
        self.name = name
        self.rules = rules
        self.stocks = map(lambda x: x[0], FTSE_100)
        self.data = shelve.open("trader_data_" + name)
        self.getter = GoogleGetter()
        if self.data.has_key('cash'):
            self.cash = self.data['cash']
        else:
            self.cash = 1000
    
    def reset(self):
        """ Reset all the data (except for the useful stuff) """
        self.cash = 1000
        for stock in self.stocks:
            stock_data = self.get_stock_data(stock)
            stock_data.reset()
            self.save_stock_data(stock, stock_data)
    
    def run(self):
        """ Run a cycle of applying rules, and updating purchases. """
        for stock in self.stocks:
            self.logger.debug("Applying rules to %s" % stock)
            stock_data = self.get_stock_data(stock)
            for rule in self.rules:
                self.logger.debug("Checking rule [%s]" % rule)
                if rule.rule_applies(stock_data):
                    self.logger.info("Rule [%s] matched..." % rule)
                    rule_result = rule.get_result(stock_data, self.cash)
                    self.logger.info("...Result: %s", rule_result)
                    self.cash -= stock_data.apply_transaction(rule_result)
                    self.save_stock_data(stock, stock_data)
        
    def update_all_stocks(self):
        """ Update the current price of all stocks, adding today's value to the database. """
        for stock in self.stocks:
            self.update_stock(stock)
            
    def update_stock(self, stock, date=None, value=None):
        """ Update the current price of a stock, adding today's value to the database. """
        # Get existing data, add today's entry, and save it back
        stock_data = self.get_stock_data(stock)
        if date == None:
            date = datetime.date.today()
        if value == None:
            value = self.getter.get_stock_value(stock)
        stock_data.add_history_value(value, date)
        self.save_stock_data(stock, stock_data)
            
    def total_stock_value(self):
        """ Get the total value of all stocks held. """
        total = 0.0
        for stock in self.stocks:
            stock_data = self.get_stock_data(stock)
            total += stock_data.last_value * stock_data.holding
        return total 
            
    def get_stock_data(self, stock):
        """ Get the stock data for a specific stock, initializing a new object if one doesn't already exist. """
        if self.data.has_key(stock):
            stock_data = self.data[stock]
            
            # Do some migration if necessary
            if not hasattr(stock_data, "logger"):
                stock_data.logger = logging.getLogger("StockData") 
        else:
            stock_data = StockData()
        return stock_data

    def save_stock_data(self, stock, stock_data):
        """ Save the data for a stock. """
        # Drop the logger first.
        temp_logger = stock_data.logger
        delattr(stock_data, "logger")
        self.data[stock] = stock_data
        stock_data.logger = temp_logger
        
        # Also save cash, as it's likely something has changed.
        self.data['cash'] = self.cash
        
    def expected_return(self):
        """ Calculate the expected return based on the stocks' increase in value """
        # Map stock names to a list of returns
        returns = []
        for stock in self.stocks:
            stock_data = self.get_stock_data(stock)
            initial_value = stock_data.initial_value()
            returns.append(100 * (stock_data.last_value - initial_value) / initial_value)
        return sum(returns) / len(returns)

    def __str__(self):
        stock_value = self.total_stock_value()
        ret_str = "Trader: %s\n\n" % self.name
        total_value = self.cash + stock_value
        ret_str += "Total value: \xa3%.2f\n\n" % total_value
        ret_str += "Cash:   \xa3%.2f\n" % self.cash
        ret_str += "Stocks: \xa3%.2f\n" % stock_value
        ret_str += "\n"
        ret_str += "Return:          %4.2f%%\n" % (100 * (total_value - 1000) / 1000)
        ret_str += "Expected Return: %4.2f%%\n" % self.expected_return()
        ret_str += "\n"        
        all_transactions = []
        for stock in self.stocks:
            stock_data = self.get_stock_data(stock)
            all_transactions.extend(map(lambda x: (stock, x), stock_data.transactions))
            if stock_data.holding > 0:
                orig_value = stock_data.sorted_holdings_value()
                stock_value = stock_data.last_value * stock_data.holding
                pct_increase = 100 * (stock_value - orig_value) / orig_value
                ret_str += "%-6s: %4d : \xa3%7.2f  (%.2f%%)\n" % (stock, stock_data.holding, stock_value, pct_increase)
        ret_str += "\n"
        for (s, t) in sorted(all_transactions, key=lambda x: x[1].date):
            ret_str += "%-4s: %s\n" % (s, t)
        return ret_str


class StockData:

    def __init__(self):
        self.logger = logging.getLogger("StockData")
        self.history = {}
        self.transactions = []
        self.holding = 0
        self.last_value = 0.0        
        
    def reset(self):
        """ Reset all data (except for the useful bits) """
        self.transactions = []
        self.holding = 0

    def apply_transaction(self, transaction):
        """ Record a transaction to buy/sell some of this stock """
        self.logger.info("Applying transaction: %s" % transaction)
        self.holding += transaction.quantity
        self.transactions.append(transaction)
        return transaction.price * transaction.quantity

    def add_history_value(self, value, date):
        """ Add (or update) today's value to the history for this stock """
        self.history[date] = value
        self.last_value = value
        
    def get_historical_value(self, days_ago, start_date=datetime.date.today()):
        """ Get the stock value from a number of days ago """
        value = -1.0
        
        # Decrement the date until we've gone back far enough - but ignore weekends
        key = start_date
        days_to_go = days_ago
        
        # Make sure the start day is the last weekday
        while key.weekday() > 4:
            key = key - datetime.timedelta(days=1)
            
        # Decrement until we've gone back far enough
        while days_to_go > 0:
            key = key - datetime.timedelta(days=1)
            days_to_go = days_to_go - 1
            
            # Decrement weekends to get the previous Friday
            while key.weekday() > 4:
                key = key - datetime.timedelta(days=1)        
        
        # Get the value if we have one
        if self.history.has_key(key):
            value = self.history[key]
        return value
    
    def sorted_holdings(self):
        """ Get a representation of the total holdings.  When sales occur, this function sells the _cheapest_ shares. """
        ret_val = []
        for transaction in self.transactions:
            if transaction.quantity > 0:
                # Purchase
                ret_val.extend([transaction.price] * transaction.quantity)
                ret_val.sort()
            else:
                # Sale - pop the cheapest shares
                ret_val = ret_val[-transaction.quantity:]
        return ret_val
    
    def sorted_holdings_value(self):
        """ Get a representation of the 'original' price of these holdings, using the sorted_holdings method. """
        return sum(self.sorted_holdings())
    
    def initial_value(self):
        """ Get the first price of the stock """
        return self.history[sorted(self.history)[0]]