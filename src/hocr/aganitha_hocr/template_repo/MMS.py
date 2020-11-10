#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Union

from src.hocr.aganitha_hocr.extractor import Extractor
from src.hocr.aganitha_hocr.filter import right, top, bot, left, nearest, get_text, nearest_by_text
from src.hocr.aganitha_hocr.matcher import Matcher
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
import re
from dateutil import *
from dateutil.parser import *
import logging

logger = logging.getLogger(__name__)


# PREDICATES

class TopRightDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, level="word")
        logger.debug("In TopRightDateChecker")
        if len(block_set.blocks) == 1:
            logger.debug("True")
            return True
        else:
            logger.debug("False")
            return False


class TopRightCheckChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        list_of_blocks = get_text(context, self.anchor,
                                  level="phrase")  # returns a List[Block] for now. Need to update.
        logger.debug("In TopRightCheckChecker")
        if len(list_of_blocks) == 2:
            logger.debug("True In TopRightCheckChecker")
            return True
        else:
            logger.debug("False In TopRightCheckChecker")
            return False


class TopRightAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        list_of_blocks = get_text(context, self.anchor,
                                  level="phrase")  # returns a List[Block] for now. Need to update.
        logger.debug("In TopRightCheckChecker")
        if len(list_of_blocks) == 2:
            logger.debug("True In TopRightCheckChecker")
            return True
        else:
            logger.debug("False In TopRightCheckChecker")
            return False


# MATCHERS

class TopRightDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightDateMatcher")
        block_set = get_text(context, "DATE:")
        if len(block_set.blocks) == 1:
            month = nearest(context, block_set.blocks[0], axis="right")
            day = nearest(context, month.blocks[0], axis="right")
            year = nearest(context, day.blocks[0], axis="right")
            logger.debug("%r", month.blocks[0].word)
            logger.debug("%r", day.blocks[0].word)
            logger.debug("%r", year.blocks[0].word)
            # Regex Validations
            if not re.match(r'[a-zA-Z]', month.blocks[0].word):
                logger.debug("Date Does Not Match Exception!!")
            # Call Helper function to convert the date format
            date = month.blocks[0].word + day.blocks[0].word + year.blocks[0].word
            date = parse(date)
            return date


class TopRightCheckMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightCheckMatcher")
        block_set = get_text(context, "NUMBER:")
        if len(block_set.blocks) == 1:
            check_num = nearest(context, block_set.blocks[0], axis="right")
            logger.debug("%r", check_num.blocks[0].word)
            # Regex Validations
            if not re.match(r'[0-9]', check_num.blocks[0].word):
                logger.debug("Exception!!!")
            return check_num.blocks[0].word


class TopRightAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> Any:
        logger.debug("In TopRightAmountMatcher")
        block_set = get_text(context, "PAID:")
        if len(block_set.blocks) == 1:
            amount = nearest(context, block_set.blocks[0], axis="right")
            logger.debug("Amount: %r", amount.blocks[0].word)
            if re.match(r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$', amount.blocks[0].word):
                return amount.blocks[0].word


class InvoiceDateMatcher(Matcher):
    pass


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
        context_check_num = right(top(context, argument=30), argument=60)
        if TopRightCheckChecker(anchor="CHECK NUMBER:").check(context_check_num):
            self.check_number = context_check_num
        status_list.append(TopRightCheckChecker(anchor="CHECK NUMBER:").check(context_check_num))

        # Check Date Match
        context_date = right(top(context, argument=30), argument=60)
        if TopRightDateChecker(anchor="DATE:").check(context_date):
            self.date = context_date
        status_list.append(TopRightDateChecker(anchor="DATE:").check(context_date))
        logger.debug("Status List: %r", status_list)

        # Check Amount Paid
        context_amount_paid = right(top(context, argument=30), argument=60)
        if TopRightAmountChecker(anchor="AMOUNT PAID:").check(context_amount_paid):
            self.amount_paid = context_amount_paid
        status_list.append(TopRightAmountChecker(anchor="AMOUNT PAID:").check(context_amount_paid))

        return all(status_list)

    def extract(self) -> List[Any]:
        extracted_params = []
        # Match And Extract Date
        date = TopRightDateMatcher().match_rule(self.date)
        extracted_params.append(date)

        # Match and Extract Check
        check_num = TopRightCheckMatcher().match_rule(self.check_number)
        extracted_params.append(check_num)

        # Match and Extract Amount Paid
        amount = TopRightAmountMatcher().match_rule(self.amount_paid)
        extracted_params.append(amount)
        return extracted_params
