#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Union, Dict

from src.hocr.aganitha_hocr.extractor import Extractor
from src.hocr.aganitha_hocr.filter import right, top, bot, left, nearest, get_text
from src.hocr.aganitha_hocr.matcher import Matcher
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
import re
from dateutil.parser import parse
import logging

logger = logging.getLogger(__name__)


# Checkers

class TopLeftCustomerNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            return True

        return False


class TopRightCheckNumberChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            return True

        return False


class TopRightCheckDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            return True

        return False


class TopRightCheckAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            return True

        return False


# Matchers

class TopRightCheckDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        context = right(top(context, argument=40), 50)
        block_set = context.get_blockset_by_query("Check Date")
        if len(block_set.blocks) == 2:
            date = nearest(context, block_set.blocks[0], axis="right")
            # Regex Validations
            if not re.match(r'\d{2}\/\d{2}\/\d{4}', date.blocks[0].word):
                logger.debug("Date Does Not Match pattern!!")
                raise Exception
            # Call Helper function to convert the date format
            date = parse(date)
            return [date]


class TopRightCheckNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:

        check_number = nearest(context,  axis="right")
        # Regex Validations
        if not re.match(r'[0-9]', check_num.blocks[0].word):
            logger.debug("Exception!!!")
        return [check_num.blocks[0].word]


class GroupM(Extractor):

    def __init__(self):
        self.check_number_blockset: BlockSet = None
        self.check_date_blockset: BlockSet = None
        self.check_amount_blockset: BlockSet = None
        self.table_header_list: List = ["Invoice Number", "Period", "Media Client/Product", "Net Amount"]
        self.invoice_number_blockset: BlockSet = None
        self.period_blockset: BlockSet = None
        self.media_client_blockset: BlockSet = None
        self.net_amount_blockset: BlockSet = None
        self.total_blockset: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list: List = []

        # customer-name match
        customer_name_context = left(top(context, argument=30), 40)
        customer_name_1_status = TopLeftCustomerNameChecker(anchor="WAVEMAKER").check(customer_name_context)
        customer_name_2_status = TopLeftCustomerNameChecker(anchor="GROUPM").check(customer_name_context)
        if customer_name_1_status or customer_name_2_status:  # append customer name status to overall status lit
            status_list.append(True)
        else:
            status_list.append(False)

        # check-number match
        check_number_context = right(top(context, argument=40), 50)
        check_number_status = TopRightCheckNumberChecker(anchor="CheckNo.").check(check_number_context)
        if check_number_status:
            self.check_number_blockset = check_number_context

        status_list.append(check_number_status)  # append check number status to overall status list

        # check-date match
        check_date_context = right(top(context, argument=40), 50)
        check_date_status = TopRightCheckDateChecker(anchor="CheckDate").check(check_date_context)
        if check_date_status:
            self.check_date_blockset = check_date_context

        status_list.append(check_date_status)  # append check date status to overall status list

        # check-amount match
        check_amount_context = right(top(context, argument=40), 50)
        check_amount_status = TopRightCheckAmountChecker(anchor="CheckAmount").check(check_amount_context)
        if check_amount_status:
            self.check_amount_blockset = check_amount_context

        status_list.append(check_amount_status)  # append check amount status to overall status list

        return True

    def extract(self, context: BlockSet) -> List[Any]:
        extracted_params = {}

        # match and extract check-number
        check_number = TopRightCheckNumberMatcher().match_rule(self.check_number_blockset)


        # match and extract check-date

        # match and extract check-amount



        return extracted_params
