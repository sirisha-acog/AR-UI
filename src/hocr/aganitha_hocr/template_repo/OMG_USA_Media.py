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
class TopLeftNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
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


class TopRightCheckNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopRightCheckAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})

        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomLeftInvoiceNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomLeftInvoiceDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        # for block in block_set:
            # print(block.word)
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class BottomInvoiceGrossAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomRightDiscountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class BottomRightNetAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


# MATCHERS -->

class TopRightDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        logger.debug("In TopRightDateMatcher")
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            date = nearest_by_query(context, named_params={'anchor': block_set.blocks[0], 'pattern': self.pattern,
                                                           'axis': "right"})
            print(date.__dict__)
            return [date.blocks[0].word]


class TopRightCheckNumberMatcher(Matcher):

    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        check_number_blockset = nearest_by_query(context,
                                                 named_params={"anchor": anchor_blockset.get_synthetic_block(),
                                                               'pattern': self.pattern,
                                                               "axis": "right"})
        return [check_number_blockset.blocks[0].word]


class TopRightCheckAmountMatcher(Matcher):

    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        check_amount_blockset = nearest_by_query(context,
                                                 named_params={"anchor": anchor_blockset.get_synthetic_block(),
                                                               'pattern': self.pattern,
                                                               "axis": "right"})
        return [check_amount_blockset.blocks[0].word.replace(" ", "")]


class BottomLeftInvoiceNumberMatcher(Matcher):
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


class BottomLeftInvoiceDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        date_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_date_blockset = get_blockset_by_anchor_axis(context,
                                                          named_params={"anchor": date_blockset.get_synthetic_block(),
                                                                        "axis": 'bot'})
        temp = []
        for block in below_date_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class BottomInvoiceGrossAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        gross_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_gross_blockset = get_blockset_by_anchor_axis(context,
                                                           named_params={"anchor": gross_blockset.get_synthetic_block(),
                                                                         "axis": 'bot'})
        discount_blockset = get_text(context, named_params={"query": 'Discount', "level": "word"})
        left_discount_blockset = get_blockset_by_anchor_axis(context,
                                                             named_params={
                                                                 "anchor": discount_blockset.get_synthetic_block(),
                                                                 "axis": 'left'})
        description_blockset = get_text(context, named_params={"query": 'Description', "level": "word"})
        right_description_blockset = get_blockset_by_anchor_axis(context,
                                                                 named_params={
                                                                     "anchor": description_blockset.get_synthetic_block(),
                                                                     "axis": 'right'})
        new_blockset = intersection(below_gross_blockset, left_discount_blockset)
        new_blockset = intersection(new_blockset, right_description_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


class BottomRightDiscountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        discount_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_discount_blockset = get_blockset_by_anchor_axis(context,
                                                              named_params={
                                                                  "anchor": discount_blockset.get_synthetic_block(),
                                                                  "axis": 'bot'})

        amount_blockset = get_text(context, named_params={"query": 'Amount', "level": "word"})
        right_amount_blockset = get_blockset_by_anchor_axis(context,
                                                            named_params={
                                                                "anchor": amount_blockset.get_synthetic_block(),
                                                                "axis": 'right'})

        net_blockset = get_text(context, named_params={"query": 'Net', "level": "word"})
        left_net_blockset = get_blockset_by_anchor_axis(context,
                                                        named_params={
                                                            "anchor": net_blockset.get_synthetic_block(),
                                                            "axis": 'left'})

        new_blockset = intersection(below_discount_blockset, right_amount_blockset)

        new_blockset = intersection(new_blockset, left_net_blockset)

        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


class BottomRightNetAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        net_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_net_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={
                                                             "anchor": net_blockset.get_synthetic_block(),
                                                             "axis": 'bot'})
        discount_blockset = get_text(context, named_params={"query": 'Net', "level": "word"})
        right_discount_blockset = get_blockset_by_anchor_axis(context,
                                                              named_params={
                                                                  "anchor": discount_blockset.get_synthetic_block(),
                                                                  "axis": 'right'})
        new_blockset = intersection(below_net_blockset, right_discount_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


# OMG Class Extractor

class OMG(Extractor):

    def __init__(self):
        self.customer_name: BlockSet = None
        self.date: BlockSet = None
        self.check_amount: BlockSet = None
        self.check_number: BlockSet = None
        self.invoice_date: BlockSet = None
        self.invoice_number: BlockSet = None
        self.amount: BlockSet = None
        self.check_total: BlockSet = None
        self.gross_amount: BlockSet = None
        self.discount: BlockSet = None
        self.net_amount: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []

        # Customer Name
        # context_customer_name = left(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        # if TopLeftNameChecker(anchor="OMG").check(context_customer_name):
        #     self.customer_name = context_customer_name
        # status_list.append(TopLeftNameChecker(anchor="OMG").check(context_customer_name))

        # Date
        context_date = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightDateChecker(anchor="DATE").check(context_date):
            self.date = context_date
        status_list.append(TopRightDateChecker(anchor="DATE").check(context_date))

        # Check Number
        context_check_number = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightCheckNumberChecker(anchor="CHECK NUMBER").check(context_check_number):
            self.check_number = context_check_number
        status_list.append(TopRightCheckNumberChecker(anchor="CHECK NUMBER").check(context_check_number))

        # Check Amount
        context_check_amount = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightCheckAmountChecker(anchor="CHECK AMOUNT").check(context_check_amount):
            self.check_amount = context_check_amount
        status_list.append(TopRightCheckAmountChecker(anchor="CHECK AMOUNT").check(context_check_amount))

        # Table Cols
        # Invoice Number
        context_inv_num = left(bot(context, named_params={'argument': 60}), named_params={'argument': 40})
        if BottomLeftInvoiceNumberChecker(anchor="Invoice Number").check(context_inv_num):
            self.invoice_number = context_inv_num
        status_list.append(BottomLeftInvoiceNumberChecker(anchor="Invoice Number").check(context_inv_num))

        # Invoice Date
        context_inv_date = left(bot(context, named_params={'argument': 60}), named_params={'argument': 50})
        if BottomLeftInvoiceDateChecker(anchor="Date").check(context_inv_date):
            self.invoice_date = context_inv_date
        status_list.append(BottomLeftInvoiceDateChecker(anchor="Date").check(context_inv_date))

        # Gross Amount
        context_gross_amount = bot(context, named_params={'argument': 60})
        if BottomInvoiceGrossAmountChecker(anchor='Gross Amount').check(context_gross_amount):
            self.gross_amount = context_gross_amount
        status_list.append(BottomInvoiceGrossAmountChecker(anchor='Gross Amount').check(context_gross_amount))

        # Discount
        context_discount = right(bot(context, named_params={'argument': 60}), named_params={'argument': 50})
        if BottomRightDiscountChecker(anchor='Discount').check(context_discount):
            self.discount = context_discount
        status_list.append(BottomRightDiscountChecker(anchor='Discount').check(context_discount))

        # Net Amount
        context_net_amount = right(bot(context, named_params={'argument': 60}), named_params={'argument': 40})
        if BottomRightNetAmountChecker(anchor='Net').check(context_net_amount):
            self.net_amount = context_net_amount
        status_list.append(BottomRightNetAmountChecker(anchor='Net').check(context_net_amount))
        # print(status_list)
        return all(status_list)

    def extract(self, context: BlockSet) -> Any:
        extracted_params = {}

        # Date at top right
        date = TopRightDateMatcher(anchor="DATE", pattern=r'^\d{2}/\d{2}/\d{4}$').match_rule(self.date)
        extracted_params["Date"] = date
        # Check number
        check_number = TopRightCheckNumberMatcher(anchor="NUMBER", pattern=r'^\d{10}$').match_rule(
            self.check_number)
        extracted_params.update({"Check Number": check_number})

        # Check Amount
        check_amount = TopRightCheckAmountMatcher(anchor="$", pattern=r'$[\d,\.]+').match_rule(
            self.check_amount)
        extracted_params.update({"Check Amount": check_amount})

        # Invoice Number
        inv_num = BottomLeftInvoiceNumberMatcher(anchor='Invoice', pattern=r'([0-9]{1,9})([\-])(\d{1})').match_rule(
            self.invoice_number)
        extracted_params.update({"Invoice Number": inv_num})

        # Invoice Date
        inv_date = BottomLeftInvoiceNumberMatcher(anchor='Invoice', pattern=r'([0-9]{1,9})$').match_rule(
            self.invoice_date)
        extracted_params.update({"Invoice Date": inv_date})

        # Gross Amount
        gross_amount = BottomInvoiceGrossAmountMatcher(anchor='Gross',
                                                       pattern=r'^([-+]?[0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?').match_rule(
            self.gross_amount)
        extracted_params.update({"Gross Amount": gross_amount})

        # Discount
        # discount_amount = BottomRightDiscountMatcher(anchor='Discount',
        #                                              pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?').match_rule(
        #     self.discount)
        # extracted_params.update({"Discount": discount_amount})

        # Net Amount
        net_amount = BottomRightNetAmountMatcher(anchor='Net',
                                                 pattern=r'^([-+]?[0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])$').match_rule(
            self.net_amount)
        extracted_params.update({"Net Amount": net_amount})
        logger.debug("Extracted Params : %r", extracted_params)
        extracted_params.update({"Customer": "OMG"})
        return extracted_params
