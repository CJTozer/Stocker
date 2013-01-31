from Trader import Trader
from Rules import * 
import logging, argparse

logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(name)-16s%(message)s',
                    filename='Stocker.log',
                    filemode = 'w',
                    level=logging.DEBUG)
logger = logging.getLogger("StockerScript")

##
## List of traders and rulesets
##
rulesets = {"default" : [], # Empty so it never buys anything
            "cjt_1" :  [Rule(rule_criterion_stock_change_days_in_a_row(3, 0.005),
                             rule_result_buy_cash_proportion(0.05),
                             description="Buy 5% of remaining cash if it increases 3 days in a row"),
                        Rule(rule_criterion_overall_holding_change(0.10),
                             rule_result_buy_stock_proportion(-0.50),
                             description="Sell 50% if value has increased by 10%"),
                        Rule(rule_criterion_overall_holding_change(-0.15),
                             rule_result_buy_stock_proportion(-0.75),
                             description="Sell 75% if value has fallen by 15%")],
            "elnt_1" : [Rule(rule_criterion_stock_change_overall(3, -0.30),
                             rule_result_buy_cash_proportion(0.10),
                             description="Buy 10% if stock drops by 30% in 3 days"),
                        Rule(rule_criterion_overall_holding_change(0.10),
                             rule_result_buy_cash_proportion(-0.20),
                             description="Sell 20% if value has increased by 10%")],
            "elnt_2" : [Rule(rule_criterion_stock_change_overall(3, -0.30),
                             rule_result_buy_cash_proportion(0.10),
                             description="Buy 10% if stock drops by 5% in 3 days"),
                        Rule(rule_criterion_overall_holding_change(0.10),
                             rule_result_buy_cash_proportion(-0.20),
                             description="Sell 20% if value has increased by 10%")]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", help="Update all stock values.", action="store_true")
    parser.add_argument("-r", "--run", help="Run the trader.", action="store_true")
    parser.add_argument("-s", "--show", help="Show the trader's current status.", action="store_true")
    parser.add_argument("--reset", help="Reset the trader's data.", action="store_true")
    parser.add_argument("-t", "--trader", help="The trader to work with.  All if not specified.")
    args = parser.parse_args()
    
    # Do all traders or just one?
    traders = sorted(rulesets.keys())
    if args.trader:
        traders = [args.trader]
    
    logger.info("Starting up")
    for trader in traders:
        logger.info("Handling trader %s", trader)
        t = Trader(rules=rulesets[trader], name=trader)
        if args.reset:
            logger.info("Resetting data")
            t.reset()
        if args.update:
            logger.info("Updating all stocks")
            t.update_all_stocks()
        if args.run:
            logger.info("Running trader")
            t.run()
        if args.show:
            print "===============================\n\n%s" % t
        
# Script entry point
if __name__ == '__main__':
    main()