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
            logger.info('Customer name found!: %r', self.anchor)
            return True

        logger.info('Customer name not found!: %r', self.anchor)
        return False


class TopRightCheckNumberChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            logger.info('String Check number found!: %r', self.anchor)
            return True

        logger.info('String Check number not found!: %r', self.anchor)
        return False


class TopRightCheckDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        logger.info('String Check date found!: %r', self.anchor)
        if len(block_set) > 0:
            return True

        logger.info('String Check date not found!: %r', self.anchor)
        return False


class TopRightCheckAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            logger.info('String Check amount found!: %r', self.anchor)
            return True

        logger.info('String Check amount not found!: %r', self.anchor)
        return False


class BotTotalAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            logger.info('String total found!: %r', self.anchor)
            return True

        logger.info('String total not found!: %r', self.anchor)
        return False


# Matchers

class TopRightCheckNumberMatcher(Matcher):

    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, self.anchor, level="word")
        check_number_blockset = nearest(context, anchor_blockset, axis="right")

        # Regex Validations
        if not re.match(self.pattern, check_number_blockset.blocks[0].word):
            logger.debug("Check number do not match pattern!")
            raise Exception
        return [check_number_blockset.blocks[0].word]


class TopRightCheckDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, self.anchor, level="word")
        check_date_blockset = nearest(context, anchor_blockset, axis="right")

        # Regex Validations
        if not re.match(self.pattern, check_date_blockset.blocks[0].word):
            logger.debug("Date Does Not Match pattern!!")
            raise Exception

        return [check_date_blockset.blocks[0].word]


class TopRightCheckAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        anchor_blockset = get_text(context, self.anchor, level="word")
        check_amount_blockset = nearest(context, anchor_blockset, axis="right")

        # Regex Validations
        if not re.match(self.pattern, check_amount_blockset.blocks[0].word):
            logger.debug("Check amount Does Not Match pattern!!")
            raise Exception

        return [check_amount_blockset.blocks[0].word]


class BotTotalAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        anchor_blockset = get_text(context, self.anchor, level="word")
        total_amount_blockset = nearest(context, anchor_blockset, axis="right")

        # Regex Validations
        if not re.match(self.pattern, total_amount_blockset.blocks[0].word):
            logger.debug("Total amount Does Not Match pattern!!")
            raise Exception

        return [total_amount_blockset.blocks[0].word]


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

        # total-amount match
        total_amount_context = bot(context, argument=20)
        total_amount_status = BotTotalAmountChecker(anchor="TOTAL").check(total_amount_context)
        if total_amount_status:
            self.total_blockset = total_amount_context

        status_list.append(total_amount_status)

        logger.debug('Results of all predicates: ', status_list)
        if all(status_list):
            return True
        else:
            return False

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        extracted_params = {}

        # match and extract check-number
        check_number = TopRightCheckNumberMatcher(anchor="CheckNo.", pattern=r'[0-9]').match_rule(
            self.check_number_blockset)
        check_number = int(check_number)  # transforming check number to integer
        extracted_params.update({"Check number": check_number})

        # match and extract check-date
        check_date = TopRightCheckDateMatcher(anchor="CheckDate", pattern=r'\d{2}\/\d{2}\/\d{4}').match_rule(
            self.check_date_blockset)
        extracted_params.update({"Check date": check_date})

        # match and extract check-amount
        check_amount = TopRightCheckAmountMatcher(anchor="CheckAmount", pattern=r'\$[\d,\.]+').match_rule(
            self.check_amount_blockset)
        check_amount = float(check_amount.replace('$', '').replace(',', ''))  # transforming check amount to float
        extracted_params.update({"Check amount": check_amount})

        # match and extract total-amount
        total_amount = BotTotalAmountMatcher(anchor="TOTAL", pattern=r'\$[\d,\.]+').match_rule(self.total_blockset)
        total_amount = float(total_amount.replace('$', '').replace(',', ''))  # transforming total amount to float
        extracted_params.update({"Total amount": total_amount})

        return extracted_params
