#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Dict

from aganitha_hocr.extractor import Extractor
from aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection, nearest_by_query
from aganitha_hocr.object_model import BlockSet
from aganitha_hocr.predicate import Predicate
from aganitha_hocr.matcher import Matcher
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


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


class TopLeftBcstChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopLeftVoucherChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopLeftGrsOrderChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        try:
            block_set = get_text(context, named_params={'query': self.anchor,
                                                        'level': "word"})
            block = block_set.get_synthetic_block()
        except ValueError:
            block_set = get_text(context, named_params={'query': '0rder',
                                                        'level': "word"})
            block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightGrsBilledChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        # print([block.word for block in context])
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightDescriptionChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class TopRightPaidAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "word"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 1:
            return True
        else:
            return False


class BottomCheckNumberChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomCheckDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 2:
            return True
        else:
            return False


class BottomTotalPaidAmountChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, named_params={'query': self.anchor,
                                                    'level': "phrase"})
        block = block_set.get_synthetic_block()
        if len(block.word.split()) == 3:
            return True
        else:
            return False


# MATCHERS -->


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


class TopLeftBcstMthMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        bcst_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_bcst_blockset = get_blockset_by_anchor_axis(context,
                                                          named_params={"anchor": bcst_blockset.get_synthetic_block(),
                                                                        "axis": 'bot'})
        temp = []
        for block in below_bcst_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopLeftVoucherMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        voucher_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_voucher_blockset = get_blockset_by_anchor_axis(context,
                                                             named_params={
                                                                 "anchor": voucher_blockset.get_synthetic_block(),
                                                                 "axis": 'bot'})
        temp = []
        for block in below_voucher_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class TopLeftGrsOrderMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        order_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_order_blockset = get_blockset_by_anchor_axis(context,
                                                           named_params={"anchor": order_blockset.get_synthetic_block(),
                                                                         "axis": 'bot'})
        try:
            adj_blockset = get_text(context, named_params={"query": 'Adj', 'level': "word"})
            left_adj_blockset = get_blockset_by_anchor_axis(context,
                                                            named_params={"anchor": adj_blockset.get_synthetic_block()
                                                                , "axis": 'left'})
        except ValueError:
            adj_blockset = get_text(context, named_params={"query": 'Ad', 'level': "word"})
            left_adj_blockset = get_blockset_by_anchor_axis(context,
                                                            named_params={"anchor": adj_blockset.get_synthetic_block()
                                                                , "axis": 'left'})
        voucher_blockset = get_text(context, named_params={"query": 'Voucher', 'level': "word"})
        right_voucher_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": voucher_blockset.get_synthetic_block(),
            "axis": 'right'})
        new_blockset = intersection(below_order_blockset, left_adj_blockset)
        new_blockset = intersection(new_blockset, right_voucher_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


class TopLeftGrsBilledMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        billed_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_billed_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": billed_blockset.get_synthetic_block(),
            "axis": 'bot'})
        try:
            adj_blockset = get_text(context, named_params={"query": 'Adj', 'level': "word"})
            right_adj_blockset = get_blockset_by_anchor_axis(context,
                                                             named_params={"anchor": adj_blockset.get_synthetic_block()
                                                                 , "axis": 'right'})
        except ValueError:
            adj_blockset = get_text(context, named_params={"query": 'Ad', 'level': "word"})
            right_adj_blockset = get_blockset_by_anchor_axis(context,
                                                             named_params={"anchor": adj_blockset.get_synthetic_block()
                                                                 , "axis": 'right'})
        adv_blockset = get_text(context, named_params={"query": 'Advertiser', 'level': 'word'})
        left_adv_blockset = get_blockset_by_anchor_axis(context,
                                                        named_params={"anchor": adv_blockset.get_synthetic_block()
                                                            , "axis": 'left'})
        new_blockset = intersection(below_billed_blockset, right_adj_blockset)
        new_blockset = intersection(new_blockset, left_adv_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


class TopRightPaidAmountMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        amount_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_amount_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": amount_blockset.get_synthetic_block(),
            "axis": 'bot'})
        description_blockset = get_text(context, named_params={"query": 'Description', "level": "word"})
        right_description_blockset = get_blockset_by_anchor_axis(context, named_params={
            "anchor": description_blockset.get_synthetic_block(),
            "axis": 'right'})
        new_blockset = intersection(below_amount_blockset, right_description_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


class BottomCheckNumberMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        number_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_num_blockset = get_blockset_by_anchor_axis(context,
                                                         named_params={"anchor": number_blockset.get_synthetic_block(),
                                                                       "axis": 'bot'})
        temp = []
        for block in below_num_blockset:
            if re.match(self.pattern, block.word):
                temp.append(block.word)
        return temp


class BottomCheckDateMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        date_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_date_blockset = get_blockset_by_anchor_axis(context,
                                                          named_params={"anchor": date_blockset.get_synthetic_block(),
                                                                        "axis": 'bot'})
        month_block = nearest_by_query(context, named_params={"anchor": date_blockset.get_synthetic_block(), "axis": "bot", "pattern": self.pattern})
        date_block = nearest_by_query(context, named_params={"anchor": date_blockset.get_synthetic_block(), "axis": "bot", "pattern": r'^\d{2}$'})
        year_block = nearest_by_query(context, named_params={"anchor": date_blockset.get_synthetic_block(), "axis": "bot", "pattern": r'^\d{4}$'})
        temp = month_block.blocks[0].word + '/' + date_block.blocks[0].word + '/' + year_block.blocks[0].word
        return [temp]


class BottomTotalAmountPaidMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        amount_blockset = get_text(context, named_params={"query": self.anchor, "level": "word"})
        below_amount_blockset = get_blockset_by_anchor_axis(context,
                                                            named_params={
                                                                "anchor": amount_blockset.get_synthetic_block(),
                                                                "axis": 'bot'})
        date_blockset = get_text(context, named_params={"query": 'Date', "level": "word"})
        right_date_blockset = get_blockset_by_anchor_axis(context,
                                                          named_params={"anchor": date_blockset.get_synthetic_block(),
                                                                        "axis": 'right'})
        new_blockset = intersection(below_amount_blockset, right_date_blockset)
        temp = []
        for block in new_blockset:
            if re.match(self.pattern, block.word.replace(" ", "")):
                temp.append(float(block.word.replace(" ", "")))
        return temp


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
        self.check_number: BlockSet = None
        self.check_date: BlockSet = None
        self.total_amount_paid: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        status_list = []
        # Customer Name
        # print(context.__dict__)
        context_customer_name = left(top(context, named_params={'argument': 50}), named_params={'argument': 40})
        # print(context_customer_name.__dict__)
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
        if TopLeftStationInvoiceChecker(anchor='Invoice').check(context_station_inv):
            self.station_inv = context_station_inv
        status_list.append(TopLeftStationInvoiceChecker(anchor='Invoice').check(context_station_inv))

        # Bcst-Mth Check
        context_bcst = left(top(context, named_params={'argument': 70}), named_params={'argument': 40})
        if TopLeftBcstChecker(anchor='Bcst').check(context_bcst):
            self.bcst_mth = context_bcst
        status_list.append(TopLeftBcstChecker(anchor='Bcst').check(context_bcst))

        # Voucher Check
        context_voucher = left(top(context, named_params={'argument': 70}), named_params={'argument': 40})
        if TopLeftVoucherChecker(anchor='Voucher').check(context_voucher):
            self.voucher = context_voucher
        status_list.append(TopLeftVoucherChecker(anchor='Voucher').check(context_voucher))

        # Grs Order Check
        context_grs_order = left(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopLeftGrsOrderChecker(anchor='Order').check(context_grs_order):
            self.grs_order = context_grs_order
        status_list.append(TopLeftGrsOrderChecker(anchor='Order').check(context_grs_order))

        # Grs Billed Check
        context_grs_billed = right(top(context, named_params={'argument': 70}), named_params={'argument': 70})
        if TopRightGrsBilledChecker(anchor='Billed').check(context_grs_billed):
            self.grs_billed = context_grs_billed
        status_list.append(TopRightGrsBilledChecker(anchor='Billed').check(context_grs_billed))

        # Description Check
        context_description = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        if TopRightDescriptionChecker(anchor='Description').check(context_description):
            self.description = context_description
        status_list.append(TopRightDescriptionChecker(anchor='Description').check(context_description))

        # Paid Amount Check
        context_paid_amount = right(top(context, named_params={'argument': 70}), named_params={'argument': 50})
        # print(context_paid_amount.__dict__)
        if TopRightPaidAmountChecker(anchor='Paid').check(context_paid_amount):
            self.paid_amount = context_paid_amount
        status_list.append(TopRightPaidAmountChecker(anchor='Paid').check(context_paid_amount))

        # Check Number Check
        context_check_number = bot(context, named_params={'argument': 30})
        if BottomCheckNumberChecker(anchor='Check No').check(context_check_number):
            self.check_number = context_check_number
        status_list.append(BottomCheckNumberChecker(anchor='Check No').check(context_check_number))

        # Check Date
        context_check_date = bot(context, named_params={'argument': 30})
        if BottomCheckDateChecker(anchor='Check Date').check(context_check_date):
            self.check_date = context_check_date
        status_list.append(BottomCheckDateChecker(anchor='Check Date').check(context_check_date))

        # Total Amount Paid
        context_total_amount_paid = bot(context, named_params={'argument': 30})
        if BottomTotalPaidAmountChecker(anchor='Total Paid Amount').check(context_total_amount_paid):
            self.total_amount_paid = context_total_amount_paid
        status_list.append(BottomTotalPaidAmountChecker(anchor='Total Paid Amount').check(context_total_amount_paid))
        # print(status_list)
        return all(status_list)

    def extract(self, context: BlockSet) -> Dict:
        extracted_params = {}

        # Stn-Invoice Number Extraction
        inv_num = TopLeftInvoiceNumberMatcher(anchor='Invoice', pattern=r'([0-9]{6,9})([\-])(\d{1})$').match_rule(
            self.station_inv)
        extracted_params['Stn-Invoice'] = inv_num

        # # Bcst-Mth Extraction
        bcst_mth = TopLeftBcstMthMatcher(anchor='Bcst',
                                         pattern=r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'?/?(\d{2})$").match_rule(
            self.bcst_mth)
        # extracted_params['Bcst-Mth'] = bcst_mth

        # Voucher Extraction
        voucher = TopLeftVoucherMatcher(anchor='Voucher', pattern=r'\d{8}$').match_rule(self.voucher)
        extracted_params['Voucher'] = voucher

        # Grs- Order Extraction
        grs_order = TopLeftGrsOrderMatcher(anchor='Order',
                                           pattern=r'^([-+]?[0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.grs_order)
        extracted_params['Grs-Order'] = grs_order

        # Grs Billed Matcher
        grs_billed = TopLeftGrsBilledMatcher(anchor='Billed',
                                             pattern=r'^([-+]?[0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.grs_billed)
        extracted_params['Grs-Billed'] = grs_billed

        # Paid amount Matcher
        paid_amount = TopRightPaidAmountMatcher(anchor='Amount',
                                                pattern=r'^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.paid_amount)
        extracted_params['Paid Amount'] = paid_amount

        # Check Number Matcher
        check_number = BottomCheckNumberMatcher(anchor='No', pattern=r'^\d{6,9}$').match_rule(self.check_number)
        extracted_params['Check Number'] = check_number[0]

        # Check Date Matcher
        check_date = BottomCheckDateMatcher(anchor='Date',
                                            pattern=r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)').match_rule(
            self.check_date)
        extracted_params['Check Date'] = check_date[0]

        # Total Amount Paid
        total = BottomTotalAmountPaidMatcher(anchor='Total',
                                             pattern=r'^([-+]?[0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$').match_rule(
            self.total_amount_paid)
        extracted_params["Total"] = total[0]
        extracted_params["Customer"] = "Katz"
        return extracted_params
