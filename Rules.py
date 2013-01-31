import datetime, logging

logger = logging.getLogger("Rules")

class Rule:
    def __init__(self, criterion, result, description="Unnamed rule"):
        self.rule_applies = criterion
        self.get_result = result
        self.description = description
        
    def __str__(self):
        return self.description

##
## Rule utlities
##
def combine_criteria_all_apply(criteria):
    def result(stock_data):
        for criterion in criteria:
            if not criterion(stock_data):
                return False
        return True
    return result

def combine_criteria_any_apply(criteria):
    def result(stock_data):
        for criterion in criteria:
            if criterion(stock_data):
                return True
        return False
    return result

##
## Rule criteria
##
def rule_criterion_stock_change_days_in_a_row(days, amount):
    """ Criterion matches if stock has increased by a given amount for a certain number of days in a row. """
    def result(stock_data):
        meets_criterion = True
        days_ago = 0
        while days_ago < days:
            this_value = stock_data.get_historical_value(days_ago)
            prev_value = stock_data.get_historical_value(days_ago + 1)
            if this_value < 0 or prev_value < 0:
                return False
            delta_ratio = (this_value / prev_value) - 1
            logger.debug("Increase [t-%d/t-%d] is %.4f" % (days_ago, days_ago + 1, delta_ratio))

            # Negative ratio fails.  Ratio > 1.0 meets criterion.
            if (delta_ratio / amount) < 1.0:
                return False
            days_ago = days_ago + 1
        return meets_criterion
    return result

def rule_criterion_stock_change_overall(days, amount):
    """ Criterion matches if stock has increased by a given amount since a certain number of days ago. """
    def result(stock_data):
        this_val = stock_data.get_historical_value(0)
        prev_val = stock_data.get_historical_value(days)
        ratio = (this_val / prev_val) - 1
        logger.debug("Increase [t/t-%d] is %.4f" % (days, ratio))
        return (ratio / amount) >= 1.0
    return result

def rule_criterion_overall_holding_change(amount):
    """ Criterion matches if the held stock value has changed by the given proportion since it was bought. """
    def result(stock_data):
        # Work out the total (overall) cost
        if stock_data.holding == 0:
            return False
        original_value = stock_data.sorted_holdings_value()
        current_value = stock_data.last_value * stock_data.holding
        increase = (current_value - original_value) / original_value
        
        # Negative ratio naturally fails.  Ratio > 1.0 meets criterion.
        logger.debug("Increase is %.4f" % increase)
        ratio = increase / amount
        return ratio >= 1.0
    return result

##
## Rule results
##
def rule_result_buy_cash_proportion(proportion):
    """ Set negative proportion for sale - but safer to use proportion of _owned_ stock! """
    def result(stock_data, cash):
        num_shares = int(cash * proportion / stock_data.last_value)
        return Transaction(num_shares, stock_data.last_value)
    return result

def rule_result_buy_stock_proportion(proportion):
    """ Set negative proportion for sale - where proportion 1.0 sells all stock. """
    def result(stock_data, cash):
        num_shares = int(stock_data.holding * proportion)
        return Transaction(num_shares, stock_data.last_value)
    return result


class Transaction:

    def __init__(self, quantity, price, date=datetime.date.today()):
        """ Purchases should have positive quantity, sales negative """
        self.date = date
        self.quantity = quantity
        self.price = price

    def cost(self):
        """ Value of the transaction """
        return self.price * self.quantity
    
    def __str__(self):
        return "[%s] %d @ \xa3%.2f" % (self.date, self.quantity, self.price)