#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Dict

from src.hocr.aganitha_hocr.extractor import Extractor
from src.hocr.aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection, nearest_by_query
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
from src.hocr.aganitha_hocr.matcher import Matcher
import re
import logging

logger = logging.getLogger(__name__)


# PREDICATES -->
class TopLeftCustomerNameChecker(Predicate):
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


class TopRightCheckChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightInvoiceDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightInvoicePeriodChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightInvoiceNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class TopRightAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class BottomRightAdvTotalChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomRightCheckTotalChecker(Predicate):
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


class TopRightInvoiceDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        inv_date_blockset = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        below_inv_date_blockset = get_blockset_by_anchor_axis(context, named_params={
            'anchor': inv_date_blockset.get_synthetic_block(), 'axis': 'bot'})

        temp = []
        for block in below_inv_date_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopRightInvoicePeriodMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        inv_period_blockset = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        below_inv_period_blockset = get_blockset_by_anchor_axis(context, named_params={
            'anchor': inv_period_blockset.get_synthetic_block(), 'axis': 'bot'})

        temp = []
        for block in below_inv_period_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopRightInvoiceNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        inv_num_blockset = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        below_inv_num_blockset = get_blockset_by_anchor_axis(context, named_params={
            'anchor': inv_num_blockset.get_synthetic_block(), 'axis': 'bot'})

        temp = []
        for block in below_inv_num_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class BottomRightCheckTotalMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        check_total_blockset = get_text(context, named_params={'query': self.anchor, 'level': "phrase"})
        check_block = check_total_blockset.get_synthetic_block()
        check_blockset = get_blockset_by_anchor_axis(context, named_params={'anchor': check_block, 'axis': 'right'})
        amount = nearest_by_query(check_blockset, named_params={'anchor': check_block, 'axis': 'right', 'pattern': self.pattern})
        return [amount.blocks[0].word]


# IPG Class Extractor

class IPG(Extractor):

    def __init__(self):
        self.customer_name: BlockSet = None
        self.date: BlockSet = None
        self.check_number: BlockSet = None
        self.invoice_date: BlockSet = None
        self.invoice_period: BlockSet = None
        self.invoice_number: BlockSet = None
        self.amount: BlockSet = None
        self.check_total: BlockSet = None
        self.adv_total: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []

        # Customer Name
        context_customer_name = left(top(context, named_params={'argument': 30}), named_params={'argument': 40})
        if TopLeftCustomerNameChecker(anchor='IPG').check(context_customer_name):
            self.customer_name = context_customer_name
        status_list.append(TopLeftCustomerNameChecker(anchor='IPG').check(context_customer_name))

        # Date
        context_date = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightDateChecker(anchor='Date:').check(context_date):
            self.date = context_date
        status_list.append(TopRightDateChecker(anchor='Date:').check(context_date))

        # Check Number
        context_check_number = right(top(context, named_params={'argument': 30}), named_params={'argument': 40})
        if TopRightCheckChecker(anchor='Check').check(context_check_number):
            self.check_number = context_check_number
        status_list.append(TopRightCheckChecker(anchor='Check').check(context_check_number))

        # Invoice Date
        context_invoice_date = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightInvoiceDateChecker(anchor='DATE').check(context_invoice_date):
            self.invoice_date = context_invoice_date
        status_list.append(TopRightInvoiceDateChecker(anchor='DATE').check(context_invoice_date))

        # Invoice Period
        context_invoice_period = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightInvoicePeriodChecker(anchor='PERIOD').check(context_invoice_period):
            self.invoice_period = context_invoice_period
        status_list.append(TopRightInvoicePeriodChecker(anchor='PERIOD').check(context_invoice_period))

        # Invoice Number
        context_invoice_num = right(top(context, named_params={'argument': 70}), named_params={'argument': 30})
        if TopRightInvoiceNumberChecker(anchor='INVOICE NUMBER').check(context_invoice_num):
            self.invoice_number = context_invoice_num
        status_list.append(TopRightInvoiceNumberChecker(anchor='INVOICE NUMBER').check(context_invoice_num))

        # Amount
        context_amount = right(top(context, named_params={'argument': 70}), named_params={'argument': 30})
        if TopRightAmountChecker(anchor='AMOUNT').check(context_amount):
            self.amount = context_amount
        status_list.append(TopRightAmountChecker(anchor='AMOUNT').check(context_amount))

        # Advertiser Total
        context_adv = bot(right(context, named_params={'argument': 50}), named_params={'argument': 60})
        if BottomRightAdvTotalChecker(anchor='Advertiser Total:').check(context_adv):
            self.adv_total = context_adv
        status_list.append(BottomRightAdvTotalChecker(anchor='Advertiser Total:').check(context_adv))

        # Check Total
        context_check_total = bot(right(context, named_params={'argument': 50}), named_params={'argument': 60})
        if BottomRightCheckTotalChecker(anchor='Check Total:').check(context_check_total):
            self.check_total = context_check_total
        status_list.append(BottomRightCheckTotalChecker(anchor='Check Total:').check(context_check_total))
        print(status_list)
        return True

    def extract(self, context: BlockSet) -> Dict:
        extracted_params = {}

        # Date
        date = TopRightDateMatcher(anchor='Date', pattern=r'\d{2}\/\d{2}\/\d{4}').match_rule(self.date)
        extracted_params["Date"] = date

        # Check Number
        check = TopRightCheckMatcher(anchor='No.', pattern=r'\d{9}').match_rule(self.check_number)
        extracted_params["Check Number"] = check

        # Invoice Date
        inv_date = TopRightInvoiceDateMatcher(anchor='DATE', pattern=r'\d{2}\/\d{2}\/\d{2}').match_rule(
            self.invoice_date)
        extracted_params["Invoice Date"] = inv_date

        # Invoice Period
        inv_period = TopRightInvoicePeriodMatcher(anchor='PERIOD', pattern=r'^\D{3}\/\d{4}').match_rule(
            self.invoice_period)
        extracted_params["Invoice Period"] = inv_period

        # Invoice Number
        inv_num = TopRightInvoiceNumberMatcher(anchor='NUMBER', pattern=r'([0-9]{6})([\-])(\d{1})$').match_rule(
            self.invoice_number)
        extracted_params["Invoice Number"] = inv_num

        # Check Total
        check_total = BottomRightCheckTotalMatcher(anchor='Check Total:', pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9])?$').match_rule(self.check_total)
        extracted_params['Check Total'] = check_total

        # Check Total

        return extracted_params
