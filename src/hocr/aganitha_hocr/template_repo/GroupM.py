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
        block_set = get_text(context, named_params={"query": self.anchor, "level": "word"})
        if len(block_set) > 0:
            logger.info('Customer name found!: %r', self.anchor)
            return True

        logger.info('Customer name not found!: %r', self.anchor)
        return False


class TopRightCheckNumberChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        if len(block_set) > 0:
            logger.info('String Check number found!: %r', self.anchor)
            return True

        logger.info('String Check number not found!: %r', self.anchor)
        return False


class TopRightCheckDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        logger.info('String Check date found!: %r', self.anchor)
        if len(block_set) > 0:
            return True

        logger.info('String Check date not found!: %r', self.anchor)
        return False


class TopRightCheckAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        if len(block_set) > 0:
            logger.info('String Check amount found!: %r', self.anchor)
            return True

        logger.info('String Check amount not found!: %r', self.anchor)
        return False


class BotTotalAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "word"})
        if len(block_set) > 0:
            logger.info('String total found!: %r', self.anchor)
            return True

        logger.info('String total not found!: %r', self.anchor)
        return False


class LeftInvoiceNumberChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        if len(block_set) > 0:
            logger.info('String Invoice Number found!: %r', self.anchor)
            return True

        logger.info('String Invoice Number not found!: %r', self.anchor)
        return False


class LeftPeriodChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "word"})
        if len(block_set) > 0:
            logger.info('String Period found!: %r', self.anchor)
            return True

        logger.info('String Period not found!: %r', self.anchor)
        return False


class LeftMediaClientChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        if len(block_set) > 0:
            logger.info('String Media Client/Product found!: %r', self.anchor)
            return True

        logger.info('String Media Client/Product not found!: %r', self.anchor)
        return False


class RightNetAmountChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        if len(block_set) > 0:
            logger.info('String Net Amount found!: %r', self.anchor)
            return True

        logger.info('String Net Amount not found!: %r', self.anchor)
        return False


# Matchers

class TopRightCheckNumberMatcher(Matcher):

    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        check_number_blockset = nearest(context, named_params={"anchor": anchor_blockset, "axis": "right"})

        # Regex Validations
        if not re.match(self.pattern, check_number_blockset.blocks[0].word):
            logger.debug("Check number do not match pattern!")
            raise Exception
        return [check_number_blockset.blocks[0].word]


class TopRightCheckDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        check_date_blockset = nearest(context, named_params={"anchor": anchor_blockset, "axis": "right"})

        # Regex Validations
        if not re.match(self.pattern, check_date_blockset.blocks[0].word):
            logger.debug("Date Does Not Match pattern!!")
            raise Exception

        return [check_date_blockset.blocks[0].word]


class TopRightCheckAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "phrase"})
        check_amount_blockset = nearest(context, named_params={"anchor": anchor_blockset, "axis": "right"})

        # Regex Validations
        if not re.match(self.pattern, check_amount_blockset.blocks[0].word):
            logger.debug("Check amount Does Not Match pattern!!")
            raise Exception

        return [check_amount_blockset.blocks[0].word]


class BotTotalAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        anchor_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        total_amount_blockset = nearest(context, named_params={"anchor": anchor_blockset, "axis": "right"})

        # Regex Validations
        if not re.match(self.pattern, total_amount_blockset.blocks[0].word):
            logger.debug("Total amount Does Not Match pattern!!")
            raise Exception

        return [total_amount_blockset.blocks[0].word]


class LeftInvoiceNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        invoice_number_blockset = get_text(context, named_params={"query": "Invoice Number", "level": "phrase"})
        total_amount_blockset = nearest(context, named_params={"anchor": anchor_blockset, "axis": "right"})

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
        customer_name_context = left(top(context, named_params={"argument": 30}), named_params={"argument": 40})
        customer_name_1_status = TopLeftCustomerNameChecker(anchor="WAVEMAKER").check(customer_name_context)
        customer_name_2_status = TopLeftCustomerNameChecker(anchor="GROUPM").check(customer_name_context)
        if customer_name_1_status or customer_name_2_status:  # append customer name status to overall status lit
            status_list.append(True)
        else:
            status_list.append(False)

        # check-number match
        check_number_context = right(top(context, named_params={"argument": 40}), named_params={"argument": 50})
        check_number_status = TopRightCheckNumberChecker(anchor="Check No.").check(check_number_context)
        if check_number_status:
            self.check_number_blockset = check_number_context

        status_list.append(check_number_status)  # append check number status to overall status list

        # check-date match
        check_date_context = right(top(context, named_params={"argument": 40}), named_params={"argument": 50})
        check_date_status = TopRightCheckDateChecker(anchor="Check Date").check(check_date_context)
        if check_date_status:
            self.check_date_blockset = check_date_context

        status_list.append(check_date_status)  # append check date status to overall status list

        # check-amount match
        check_amount_context = right(top(context, named_params={"argument": 40}), named_params={"argument": 50})
        check_amount_status = TopRightCheckAmountChecker(anchor="Check Amount").check(check_amount_context)
        if check_amount_status:
            self.check_amount_blockset = check_amount_context

        status_list.append(check_amount_status)  # append check amount status to overall status list

        # total-amount match
        total_amount_context = bot(context, named_params={"argument": 20})
        total_amount_status = BotTotalAmountChecker(anchor="TOTAL").check(total_amount_context)
        if total_amount_status:
            self.total_blockset = total_amount_context

        status_list.append(total_amount_status)

        # invoice-number match
        invoice_number_context = left(context, named_params={"argument": 20})
        invoice_number_status = LeftInvoiceNumberChecker(anchor="Invoice Number").check(invoice_number_context)
        if invoice_number_status:
            self.invoice_number_blockset = invoice_number_context

        status_list.append(invoice_number_status)

        # period match
        period_context = left(context, named_params={"argument": 40})
        period_status = LeftPeriodChecker(anchor="Period").check(period_context)
        if period_status:
            self.period_blockset = period_context

        status_list.append(period_status)

        # media-client match
        media_client_context = left(context, named_params={"argument": 40})
        media_client_status = LeftMediaClientChecker(anchor="Media Client/Product").check(period_context)
        if media_client_status:
            self.media_client_blockset = media_client_context

        status_list.append(media_client_status)

        # net-amount match
        net_amount_context = right(context, named_params={"argument": 40})
        net_amount_status = RightNetAmountChecker(anchor="Net Amount").check(net_amount_context)
        if net_amount_status:
            self.net_amount_blockset = net_amount_context

        # table-header match

        status_list.append(net_amount_status)

        logger.debug('Results of all predicates: ', *status_list)
        if all(status_list):
            return True
        else:
            return False

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        extracted_params = {}

        # match and extract check-number
        check_number = TopRightCheckNumberMatcher(anchor="Check No.", pattern=r'[0-9]').match_rule(
            self.check_number_blockset)
        check_number = int(check_number)  # transforming check number to integer
        extracted_params.update({"Check number": check_number})

        # match and extract check-date
        check_date = TopRightCheckDateMatcher(anchor="Check Date", pattern=r'\d{2}\/\d{2}\/\d{4}').match_rule(
            self.check_date_blockset)
        extracted_params.update({"Check date": check_date})

        # match and extract check-amount
        check_amount = TopRightCheckAmountMatcher(anchor="Check Amount", pattern=r'\$[\d,\.]+').match_rule(
            self.check_amount_blockset)
        check_amount = float(check_amount.replace('$', '').replace(',', ''))  # transforming check amount to float
        extracted_params.update({"Check amount": check_amount})

        # match and extract total-amount
        total_amount = BotTotalAmountMatcher(anchor="TOTAL", pattern=r'\$[\d,\.]+').match_rule(self.total_blockset)
        total_amount = float(total_amount.replace('$', '').replace(',', ''))  # transforming total amount to float
        extracted_params.update({"Total amount": total_amount})

        # match and extract invoice-number
        invoice_number = LeftInvoiceNumberMatcher(anchor="Invoice Number", pattern=r'\d{6}[-\d]{1}[\d\w]+').match_rule(
            self.invoice_number_blockset)
        extracted_params.update({"Invoice number": invoice_number})

        # match and extract period
        period = LeftPeriodMatcher(anchor="Period", pattern=r'\d{2}\/\d{2}\/\d{4}').match_rule(
            self.period_blockset)
        extracted_params.update({"Period": period})

        # match and extract media-client
        media_client = LeftMediaClientMatcher(anchor="Media Client/Product").match_rule(self.media_client_blockset)
        extracted_params.update({"Media Client/Product": media_client})

        # match and extract net amount
        net_amount = RightNetAmountMatcher(anchor="Net Amount").match_rule(self.net_amount_blockset)
        # net_amount = float(net_amount.replace('$', '').replace(',', ''))  # transforming net amount to float
        extracted_params.update({"Net Amount": net_amount})

        return extracted_params
