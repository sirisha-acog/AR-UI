#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
import csv
import json
from typing import Any, List, Dict

from src.hocr.aganitha_hocr.extractor import Extractor
from src.hocr.aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection, nearest_by_query
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
from src.hocr.aganitha_hocr.matcher import Matcher
import re
import logging
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

logger = logging.getLogger(__name__)


# PREDICATES -->
class TopLeftCustomerNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopRightDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightCheckChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopLeftClientNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopLeftInvoiceDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopLeftInvoiceNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopLeftBillPeriodChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopRightGrossChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightDiscountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightNetChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        for block in block_set:
            print(block.word)
        block = block_set.get_synthetic_block()
        print(block.word.split())
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightNetLessDiscountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 3:
            return True
        else:
            return False


# MATCHERS -->


# 22Squared Extractor

class Squared(Extractor):
    def __init__(self):
        self.customer_name: BlockSet = None
        self.date: BlockSet = None
        self.check_number = None
        # Table Headers
        self.client_name: BlockSet = None
        self.inv_date: BlockSet = None
        self.inv_num: BlockSet = None
        self.bill_period: BlockSet = None
        self.gross: BlockSet = None
        self.discount: BlockSet = None
        self.net: BlockSet = None
        self.net_Less_discount: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []

        # Customer Name
        context_customer_name = left(top(context, named_params={'argument': 40}), named_params={'argument': 30})
        if TopLeftCustomerNameChecker(anchor='22squared, inc.').check(context_customer_name):
            self.customer_name = context_customer_name
        status_list.append(TopLeftCustomerNameChecker(anchor='22squared, inc.').check(context_customer_name))

        # Date
        context_date = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightDateChecker(anchor='Date').check(context_date):
            self.date = context_date
        status_list.append(TopRightDateChecker(anchor='Date').check(context_date))

        # Check Number
        context_check_number = right(top(context, named_params={'argument': 30}), named_params={'argument': 40})
        if TopRightCheckChecker(anchor='Check').check(context_check_number):
            self.check_number = context_check_number
        status_list.append(TopRightCheckChecker(anchor='Check').check(context_check_number))

        # Client Name Table Header
        context_client_name = left(top(context, named_params={'argument': 70}), named_params={'argument': 40})
        if TopLeftClientNameChecker(anchor='Client Name').check(context_client_name):
            self.client_name = context_client_name
        status_list.append(TopLeftClientNameChecker(anchor='Client Name').check(context_client_name))

        # Invoice Date
        context_invoice_date = left(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopLeftInvoiceDateChecker(anchor='Inv Date').check(context_invoice_date):
            self.inv_date = context_invoice_date
        status_list.append(TopLeftInvoiceDateChecker(anchor='Inv Date').check(context_invoice_date))

        # Invoice Number
        context_invoice_num = left(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopLeftInvoiceNumberChecker(anchor='Inv. #').check(context_invoice_num):
            self.inv_num = context_invoice_num
        status_list.append(TopLeftInvoiceNumberChecker(anchor='Inv. #').check(context_invoice_num))

        # Bill Period
        context_bill_period = left(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopLeftBillPeriodChecker(anchor='Bill Prd').check(context_bill_period):
            self.bill_period = context_bill_period
        status_list.append(TopLeftBillPeriodChecker(anchor='Bill Prd').check(context_bill_period))

        # Gross Amount
        context_gross = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightGrossChecker(anchor='Gross').check(context_gross):
            self.gross = context_gross
        status_list.append(TopRightGrossChecker(anchor='Gross').check(context_gross))

        # Net Amount
        context_net = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightNetChecker(anchor='Net').check(context_net):
            self.net = context_net
        status_list.append(TopRightNetChecker(anchor='Net').check(context_net))

        # Net Less Discount
        context_net_less = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightNetLessDiscountChecker(anchor='Net Less Disc').check(context_net_less):
            self.net_Less_discount = context_net_less
        status_list.append(TopRightNetLessDiscountChecker(anchor='Net Less Disc').check(context_net_less))

        print(status_list)
        return True

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        extracted_params = {}
        return extracted_params
