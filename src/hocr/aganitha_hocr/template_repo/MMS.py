#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Dict

from src.hocr.aganitha_hocr.extractor import Extractor
from src.hocr.aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
from src.hocr.aganitha_hocr.matcher import Matcher
import re
import logging

logger = logging.getLogger(__name__)


# PREDICATES

class TopRightDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        logger.debug("In TopRightDateChecker")
        if len(block_set.blocks) == 1:
            logger.debug("True")
            return True
        else:
            logger.debug("False")
            return False


class TopRightCheckChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        logger.debug("In TopRightCheckChecker")
        if len(block.word.split()) == 2:
            logger.debug("True In TopRightCheckChecker")
            return True
        else:
            logger.debug("False In TopRightCheckChecker")
            return False


class TopRightAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        logger.debug("In TopRightCheckChecker")
        if len(block.word.split()) == 2:
            logger.debug("True In TopRightCheckChecker")
            return True
        else:
            logger.debug("False In TopRightCheckChecker")
            return False


class BottomLeftInvoiceDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        logger.debug("In BottomLeftInvoiceDateChecker")
        if len(block.word.split()) == 2:
            logger.debug("True In BottomLeftInvoiceDateChecker")
            return True
        else:
            logger.debug("False In BottomLeftInvoiceDateChecker")
            return False


class BottomLeftInvoiceNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        logger.debug("In BottomLeftInvoiceNumberChecker")
        if len(block.word.split()) == 2:
            logger.debug("True In BottomLeftInvoiceNumberChecker")
            return True
        else:
            logger.debug("False In BottomLeftInvoiceNumberChecker")
            return False


class BottomRightAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        logger.debug("In BottomRightAmountChecker")
        if len(block_set.blocks) == 1:
            logger.debug("True in BottomRightAmountChecker")
            return True
        else:
            logger.debug("False in BottomRightAmountChecker")
            return False


# MATCHERS

class TopRightDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightDateMatcher")
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            month = nearest(context, named_params={'anchor': block_set.blocks[0], 'axis': "right"})
            day = nearest(context, named_params={'anchor': month.blocks[0], 'axis': "right"})
            year = nearest(context, named_params={'anchor': day.blocks[0], 'axis': "right"})
            logger.debug("%r", month.blocks[0].word)
            logger.debug("%r", day.blocks[0].word)
            logger.debug("%r", year.blocks[0].word)
            # Regex Validations
            if not re.match(self.pattern, month.blocks[0].word):
                logger.debug("Date Does Not Match Exception!!")
            # Call Helper function to convert the date format
            date = month.blocks[0].word + " " + day.blocks[0].word + " " + year.blocks[0].word
            return date


class TopRightCheckMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightCheckMatcher")
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            check_num = nearest(context, named_params={'anchor': block_set.blocks[0], 'axis': "right"})
            logger.debug("%r", check_num.blocks[0].word)
            # Regex Validations
            if not re.match(self.pattern, check_num.blocks[0].word):
                logger.debug("Exception!!!")
            return check_num.blocks[0].word


class TopRightAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightAmountMatcher")
        block_set = get_text(context, named_params={'query': self.anchor, 'level': "word"})
        if len(block_set.blocks) == 1:
            amount = nearest(context, named_params={'anchor': block_set.blocks[0], 'axis': "right"})
            logger.debug("Amount: %r", amount.blocks[0].word)
            if re.match(self.pattern, amount.blocks[0].word):
                return amount.blocks[0].word


class BottomLeftInvoiceDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        logger.debug("In BottomLeftInvoiceDateMatcher")
        temp = []
        for block in context.blocks:
            if re.search(self.pattern, block.word):
                temp.append(block.word)
        return temp


class BottomLeftInvoiceNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        temp = []
        for block in context.blocks:
            if re.search(self.pattern, block.word):
                temp.append(block.word)
        return temp


class BottomRightAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        amount_blockset = get_text(context=context, named_params={'query': self.anchor, 'level': "word"})
        amount_blockset = amount_blockset.get_synthetic_blockset()
        amount_blockset_context = get_blockset_by_anchor_axis(context=context,
                                                              named_params={'anchor': amount_blockset.blocks[0],
                                                                            'axis': "bot"})
        total_blockset = get_text(context=context, named_params={'query': "TOTALS", 'level': "word"})
        print([block.word for block in context.blocks])
        total_blockset = total_blockset.get_synthetic_blockset()
        total_blockset_context = get_blockset_by_anchor_axis(context=context,
                                                             named_params={'anchor': total_blockset.blocks[0],
                                                                           'axis': "top"})
        print("amount : ", amount_blockset_context.__dict__)

        amount_column_context = intersection(amount_blockset_context, total_blockset_context)
        temp = []
        for block in amount_column_context.blocks:
            if re.search(self.pattern, block.word):
                temp.append(block.word)
        return temp


# MMS Class Extractor

class MMS(Extractor):

    def __init__(self):
        self.date: BlockSet = None
        self.check_number: BlockSet = None
        self.amount_paid: BlockSet = None
        self.paid_on_behalf_of: BlockSet = None
        self.table_header = ["Invoice Date", "Invoice Number", "Amount"]
        self.invoice_date: BlockSet = None
        self.invoice_number: BlockSet = None
        self.amount: BlockSet = None
        self.total: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []

        # Check Number Match
        context_check_num = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightCheckChecker(anchor="CHECK NUMBER:").check(context_check_num):
            self.check_number = context_check_num
        status_list.append(TopRightCheckChecker(anchor="CHECK NUMBER:").check(context_check_num))

        # Check Date Match
        context_date = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightDateChecker(anchor="DATE:").check(context_date):
            self.date = context_date
        status_list.append(TopRightDateChecker(anchor="DATE:").check(context_date))
        logger.debug("Status List: %r", status_list)

        # Check Amount Paid
        context_amount_paid = right(top(context, named_params={'argument': 30}), named_params={'argument': 60})
        if TopRightAmountChecker(anchor="AMOUNT PAID:").check(context_amount_paid):
            self.amount_paid = context_amount_paid
        status_list.append(TopRightAmountChecker(anchor="AMOUNT PAID:").check(context_amount_paid))

        # Check Invoice date in table
        context_invoice_date = left(bot(context, named_params={'argument': 60}), named_params={'argument': 60})
        if BottomLeftInvoiceDateChecker(anchor="Invoice Date").check(context_invoice_date):
            self.invoice_date = context_invoice_date
        status_list.append(BottomLeftInvoiceDateChecker(anchor="Invoice Date").check(context_invoice_date))

        # Check invoice number in table
        context_invoice_number = left(bot(context, named_params={'argument': 60}), named_params={'argument': 60})
        if BottomLeftInvoiceNumberChecker(anchor="Invoice Number").check(context_invoice_number):
            self.invoice_number = context_invoice_number
        status_list.append(BottomLeftInvoiceNumberChecker(anchor="Invoice Number").check(context_invoice_number))

        # Check Amount in table
        context_amount_in_table = bot(context, named_params={'argument': 90})
        if BottomRightAmountChecker(anchor="Amount").check(context_amount_in_table):
            self.amount = context_amount_in_table
        status_list.append(BottomRightAmountChecker(anchor="Amount").check(context_amount_in_table))

        return all(status_list)

    def extract(self, context: BlockSet) -> Dict:
        extracted_params = {}
        # Match And Extract Date
        date = TopRightDateMatcher(anchor="DATE:", pattern=r'[a-zA-Z]').match_rule(self.date)
        extracted_params["DATE"] = date
        print(date)
        # Match and Extract Check
        check_num = TopRightCheckMatcher(anchor="NUMBER:", pattern=r'[0-9]').match_rule(self.check_number)
        extracted_params["CHECK NUMBER"] = check_num
        print(check_num)
        # Match and Extract Amount Paid
        amount = TopRightAmountMatcher(anchor="PAID:",
                                       pattern=r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.amount_paid)
        extracted_params["AMOUNT PAID"] = amount
        print(amount)
        # Match Invoice Date
        inv_date = BottomLeftInvoiceDateMatcher(anchor="Date", pattern=r'(\d{2})[/.-](\d{2})[/.-](\d{2})$').match_rule(
            self.invoice_date)
        extracted_params["Invoice Date"] = inv_date
        print(inv_date)
        # Match Invoice Number
        inv_num = BottomLeftInvoiceNumberMatcher(anchor="Number", pattern=r'([A-Z]?)([0-9]{1,9})([\-])(\d{1})$').match_rule(
            self.invoice_number)
        extracted_params["Invoice Number"] = inv_num
        print(inv_num)
        # Match Amount in table
        amount_in_table = BottomRightAmountMatcher(anchor="Amount",
                                                   pattern=r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.amount)
        extracted_params["Amount"] = amount_in_table
        return extracted_params
