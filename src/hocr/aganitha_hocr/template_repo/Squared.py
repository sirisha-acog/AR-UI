#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
import csv
import json
from typing import Any, List, Dict

from aganitha_hocr.extractor import Extractor
from aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection, nearest_by_query
from aganitha_hocr.object_model import BlockSet
from aganitha_hocr.predicate import Predicate
from aganitha_hocr.matcher import Matcher
import re
import logging
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

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
        # for block in block_set:
        #     print(block.word)
        block = block_set.get_synthetic_block()
        # print(block.word.split())
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


class BotCheckTotalChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


# MATCHERS -->
class TopRightDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            date = nearest_by_query(context, named_params={'anchor': block_set.blocks[0], 'pattern': self.pattern,
                                                           'axis': "right"})
            return [date.blocks[0].word]


class TopRightCheckMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            check = nearest_by_query(context, named_params={'anchor': block_set.blocks[0], 'pattern': self.pattern,
                                                            'axis': "right"})
            return [check.blocks[0].word]


class TopLeftInvoiceDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        inv_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_inv_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={"anchor": inv_blockset.get_synthetic_block(),
                                                                       "axis": 'bot'})
        temp = []
        for block in below_inv_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopLeftInvoiceNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        inv_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_inv_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={"anchor": inv_blockset.get_synthetic_block(),
                                                                       "axis": 'bot'})
        temp = []
        for block in below_inv_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopRightGrossAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        gross_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_gross_blockset = get_blockset_by_anchor_axis(context,
                                                           named_params={"anchor": gross_blockset.get_synthetic_block(),
                                                                         'axis': 'bot'})
        discount_blockset = get_text(context, named_params={'query': 'Discount', "level": "word"})
        left_discount_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": discount_blockset.get_synthetic_block(), 'axis': 'left'})

        new_blockset = intersection(below_gross_blockset, left_discount_blockset)

        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(block.word.replace(" ", ""))
        return temp


class TopRightDiscountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        discount_blockset = get_text(context, named_params={'query': self.anchor, "level": "word"})
        below_discount_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": discount_blockset.get_synthetic_block(), 'axis': 'bot'})
        gross_blockset = get_text(context, named_params={"query": 'Gross', "level": "word"})
        right_gross_blockset = get_blockset_by_anchor_axis(context,
                                                           named_params={"anchor": gross_blockset.get_synthetic_block(),
                                                                         'axis': 'right'})
        net_blockset = get_text(context, named_params={"query": 'Net', "level": "word"})
        left_net_blockset = get_blockset_by_anchor_axis(context,
                                                        named_params={"anchor": net_blockset.get_synthetic_block(),
                                                                      'axis': 'left'})

        new_blockset = intersection(below_discount_blockset, right_gross_blockset)
        new_blockset = intersection(new_blockset, left_net_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(block.word.replace(" ", ""))
        return temp


class TopRightNetMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        net_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_net_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={"anchor": net_blockset.get_synthetic_block(),
                                                                       'axis': 'bot'})
        discount_blockset = get_text(context, named_params={'query': 'Discount', "level": "word"})
        right_discount_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": discount_blockset.get_synthetic_block(), 'axis': 'right'})

        less_blockset = get_text(context, named_params={'query': 'Less', "level": "word"})
        left_less_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": less_blockset.get_synthetic_block(), 'axis': 'left'})

        new_blockset = intersection(below_net_blockset, right_discount_blockset)
        new_blockset = intersection(new_blockset, left_less_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(block.word.replace(" ", ""))
        return temp


class TopRightNetLessDiscMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        less_blockset = get_text(context, named_params={'query': self.anchor, "level": "word"})
        below_less_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": less_blockset.get_synthetic_block(), 'axis': 'bot'})

        net_blockset = get_text(context, named_params={"query": "Net", "level": "word"})
        right_net_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={"anchor": net_blockset.get_synthetic_block(),
                                                                       'axis': 'right'})
        new_blockset = intersection(below_less_blockset, right_net_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(block.word.replace(" ", ""))
        return temp


class BotCheckTotalMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        total_blockset = get_text(context, named_params={'query': self.anchor, "level": "word"})
        colon = nearest(context, named_params={'anchor': total_blockset.get_synthetic_block(), 'axis': 'right'})
        gross_amount = nearest(context, named_params={'anchor': colon.get_synthetic_block(), 'axis': 'right'})
        discount_amount = nearest(context, named_params={'anchor': gross_amount.get_synthetic_block(), 'axis': 'right'})
        net_amount = nearest(context, named_params={'anchor': discount_amount.get_synthetic_block(), 'axis': 'right'})
        net_less_discount = nearest(context, named_params={'anchor': net_amount.get_synthetic_block(), 'axis': 'right'})
        return [gross_amount.blocks[0].word.replace(" ", ""), discount_amount.blocks[0].word.replace(" ", ""), net_amount.blocks[0].word.replace(" ", ""),
                net_less_discount.blocks[0].word.replace(" ", "")]


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
        self.check_total: BlockSet = None

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

        # Discount
        context_discount = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightDiscountChecker(anchor='Discount').check(context_discount):
            self.discount = context_discount
        status_list.append(TopRightDiscountChecker(anchor='Discount').check(context_discount))

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

        # Check Total
        context_check_total = bot(context, named_params={'argument': 30})
        if BotCheckTotalChecker(anchor='Check Total:').check(context_check_total):
            self.check_total = context_check_total
        status_list.append(BotCheckTotalChecker(anchor='Check Total:').check(context_check_total))

        return all(status_list)

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        extracted_params = {}
        # Date
        date = TopRightDateMatcher(anchor='Date', pattern=r'\d{2}\/\d{2}\/\d{4}').match_rule(self.date)
        extracted_params["Date"] = date

        # Check Number
        check = TopRightCheckMatcher(anchor='Check', pattern=r'\d{9}').match_rule(self.check_number)
        extracted_params["Check Number"] = check

        # Invoice Date
        inv_date = TopLeftInvoiceDateMatcher(anchor='Inv', pattern=r'\d{2}\/\d{2}\/\d{2}').match_rule(self.inv_date)
        extracted_params["Invoice Date"] = inv_date

        # Invoice Number
        inv_num = TopLeftInvoiceNumberMatcher(anchor='Inv.', pattern=r'([0-9]{1,9})([\-])(\d{1})$').match_rule(
            self.inv_num)
        extracted_params["Invoice Number"] = inv_num

        # Gross Amount
        gross_amount = TopRightGrossAmountMatcher(anchor='Gross',
                                                  pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.gross)
        extracted_params["Gross Amount"] = gross_amount

        # Discount
        discount = TopRightDiscountMatcher(anchor='Discount',
                                           pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.discount)
        extracted_params["Discount"] = discount

        # Net
        net = TopRightNetMatcher(anchor='Net',
                                 pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.net)
        extracted_params["Net"] = net

        # Net Less Discount
        net_less_disc = TopRightNetLessDiscMatcher(anchor='Less',
                                                   pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.net_Less_discount)
        extracted_params["Net Less Discount"] = net_less_disc

        # Check Totals
        check_total = BotCheckTotalMatcher(anchor="Total",
                                           pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.check_total)
        extracted_params["Gross Total"] = [check_total[0]]
        extracted_params["Discount Total"] = [check_total[1]]
        extracted_params["Net Total"] = [check_total[2]]
        extracted_params["Net Less Discount Total"] = [check_total[3]]

        return extracted_params
