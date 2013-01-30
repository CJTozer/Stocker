from Trader import Trader
from Rules import * 
import logging

logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(name)-16s%(message)s',
                    filename='Stocker.log',
                    filemode = 'w',
                    level=logging.DEBUG)
logger = logging.getLogger("StockerScript")

##
## List of rules
##
rules = [Rule(rule_criterion_stock_change(3, 0.005),
              rule_result_buy_cash_proportion(0.05),
              description="Buy 5% of remaining cash if it increases 3 days in a row"),
         Rule(rule_criterion_overall_change(0.10),
              rule_result_buy_stock_proportion(-0.50),
              description="Sell 50% if value has increased by 10%"),
         Rule(rule_criterion_overall_change(-0.15),
              rule_result_buy_stock_proportion(-0.75),
              description="Sell 75% if value has fallen by 15%")]

def main():
    logger.info("Starting up")  
    t = Trader(rules=rules)
    logger.info("Updating all stocks")
    t.update_all_stocks()
    logger.info("Running trader")
    t.run()
    print "%s" % t
        

# Script entry point
if __name__ == '__main__':
    main()