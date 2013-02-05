import unittest, logging, datetime
from Stocker.Rules import *

logging.basicConfig(format='%(asctime)s\t%(levelname)s:\t%(name)-16s%(message)s',
                    filename='Test.log',
                    filemode = 'w',
                    level=logging.DEBUG)
logger = logging.getLogger("RulesTest001")

class RulesTest001(unittest.TestCase):
    """ Basic tests of Rules. """

    def test_rule_always_matches(self):
        """ Rule always matches """
        r = Rule(rule_criterion_true(), rule_result_basic(None))
        self.assertTrue(r.rule_applies(None))
        
    def test_rule_never_matches(self):
        """ Rule never matches """
        r = Rule(rule_criterion_false(), rule_result_basic(None))
        self.assertFalse(r.rule_applies(None))
        
    def test_rules_all_apply(self):
        """ Rule combinations - all apply """
        criteria = [rule_criterion_true()] * 5
        r1 = Rule(combine_criteria_all_apply(criteria), rule_result_basic(None))
        self.assertTrue(r1.rule_applies(None))
        
        criteria[3] = rule_criterion_false()
        r2 = Rule(combine_criteria_all_apply(criteria), rule_result_basic(None))
        self.assertFalse(r2.rule_applies(None))
        
    def test_rules_any_apply(self):
        """ Rule combinations - any apply """
        criteria = [rule_criterion_false()] * 5
        r1 = Rule(combine_criteria_any_apply(criteria), rule_result_basic(None))
        self.assertFalse(r1.rule_applies(None))
        
        criteria[3] = rule_criterion_true()
        r2 = Rule(combine_criteria_any_apply(criteria), rule_result_basic(None))
        self.assertTrue(r2.rule_applies(None))
        
    
##
## Utilities
##
def rule_criterion_true():
    """ Always matches """
    def result(stock_data):
        return True
    return result

def rule_criterion_false():
    """ Never matches """
    def result(stock_data):
        return False
    return result

def rule_result_basic(return_transaction):
    """ Return the transaction passed in as a parameter """
    def result(stock_data, cash):
        return return_transaction
    return result

if __name__ == '__main__':
    unittest.main()