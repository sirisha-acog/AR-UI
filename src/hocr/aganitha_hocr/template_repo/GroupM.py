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


class TopLeftCustomerNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        context = left(top(context, argument=40), 30)
        for query in ["GROUPM", "WAVEMAKER"]:
            block_set = context.get_blockset_by_query(query)
            if len(block_set.blocks) == 1:
                return True

        return False





class TopRightDateMatcher(Matcher):
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


class TopRightCheckMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[Any]:
        context = right(top(context, argument=30), 30)
        block_set = context.get_blockset_by_query("Check No.")
        if len(block_set.blocks) == 2:
            check_num = nearest(context, block_set.blocks[0], axis="right")
            # Regex Validations
            if not re.match(r'[0-9]', check_num.blocks[0].word):
                logger.debug("Exception!!!")
            return [check_num.blocks[0].word]


class GroupM(Extractor):

    def __init__(self):
        top_right_checknumber_checker = self.TopRightCheckNumberChecker(anchor={"CheckNo.": []})
        top_right_date_checker = self.TopRightDateChecker(anchor={"CheckDate": []})

        self.check_number = top_right_checknumber_checker.anchor
        self.check_date = top_right_date_checker.anchor


        self.check_amount = {"CheckAmount": []}
        self.table_header = {"Invoice Number": [], "Period": [],
                             "Media Client/Product": [], "Net Amount": []}
        self.total = {"TOTAL": []}

        self.predicate_list = [top_right_checknumber_checker, top_right_date_checker]
        self.matched_list = []

    def match(self, context: BlockSet) -> bool:
        for predicate in self.predicate_list:
            if not predicate.check(context):
                status = False
                return status
        status = True
        return status

    def extract(self, context: BlockSet) -> List[Any]:
        extracted_params = {}
        for match in self.matched_list:
            extracted_params.append(match.match_rule(context))
        return extracted_params

    class TopRightCheckNumberChecker(Predicate):

        def check(self, context: BlockSet) -> bool:
            context = right(top(context, argument=40), 50)
            # block_set = context.get_blockset_by_query(list(self.anchor.keys())[0])
            string_set, block_set = get_text(context, list(self.anchor.keys())[0], "word")

            if len(string_set) > 0:
                self.anchor.update({list(self.anchor.keys())[0]: block_set})
                return True
            else:
                return False

    class TopRightDateChecker(Predicate):

        def check(self, context: BlockSet) -> bool:
            context = right(top(context, argument=40), 50)
            block_set = context.get_blockset_by_query(list(self.anchor.keys())[0])
            string_set = get_text(block_set, list(self.anchor.keys())[0], "word")

            if len(string_set) > 0:
                self.anchor.update({list(self.anchor.keys())[0]: block_set})
                return True
            else:
                return False
