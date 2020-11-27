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


# PREDICATES -->
class TopLeftCustomerNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 3:
            return True
        else:
            return False


class TopRightPayeeChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopLeftStationNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopLeftStationInvoiceChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False

# MATCHERS -->

# Katz Class Extractor

class Katz(Extractor):

    def __init__(self):
        self.customer_name: BlockSet = None
        self.payee: BlockSet = None
        # Table Headers
        self.station: BlockSet = None
        self.station_inv: BlockSet = None
        self.bcst_mth: BlockSet = None
        self.voucher: BlockSet = None
        self.grs_order: BlockSet = None
        self.grs_billed: BlockSet = None
        self.description: BlockSet = None
        self.paid_amount: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []
        # Customer Name
        context_customer_name = left(top(context, named_params={'argument': 30}), named_params={'argument': 40})
        if TopLeftCustomerNameChecker(anchor='Katz Media Group').check(context_customer_name):
            self.customer_name = context_customer_name
        status_list.append(TopLeftCustomerNameChecker(anchor='Katz Media Group').check(context_customer_name))

        # Payee Check
        context_payee = right(top(context, named_params={'argument': 30}), named_params={'argument': 40})
        if TopRightPayeeChecker(anchor='Payee:').check(context_payee):
            self.payee = context_payee
        status_list.append(TopRightPayeeChecker(anchor='Payee:').check(context_payee))

        # Station Check
        context_station = left(top(context, named_params={'argument': 70}), named_params={'argument': 40})
        if TopLeftStationNameChecker(anchor='Station').check(context_station):
            self.station = context_station
        status_list.append(TopLeftStationNameChecker(anchor='Station').check(context_station))

        # StationInvoice Check
        context_station_inv = left(top(context, named_params={'argument': 70}), named_params={'argument': 40})
        if TopLeftStationInvoiceChecker(anchor='Stn-Invoice').check(context_station_inv):
            self.station_inv = context_station_inv
        status_list.append(TopLeftStationInvoiceChecker(anchor='Stn-Invoice').check(context_station_inv))
        print(status_list)
        return True

    def extract(self, context: BlockSet) -> Dict:
        extracted_params = {}
        return extracted_params
