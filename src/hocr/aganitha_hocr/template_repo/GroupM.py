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


class TopRightCheckNumberChecker(Predicate):

    def check(self, context: BlockSet) -> bool:
        block_set = get_text(context, self.anchor, "word")
        if len(block_set) > 0:
            return True

        return False


class TopRightDateChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        context = right(top(context, argument=40), 50)
        for key, value in self.anchor.items():
            string_set, block_set = get_text(context, key, "word")

            if len(string_set) > 0:
                self.anchor.update({key: block_set})
                return True

        return False


class TopLeftCustomerNameChecker(Predicate):
    def check(self, context: BlockSet) -> bool:
        context = left(top(context, argument=40), 30)
        for key, value in self.anchor.items():
            string_set, block_set = get_text(context, key, "word")

            if len(string_set) > 0:
                self.anchor.update({key: block_set})
                return True

        return False


class GroupM(Extractor):

    def __init__(self):
        self.check_number = None
        self.check_date = None

        self.check_amount = {"CheckAmount": []}
        self.table_header = {"column": ["Invoice Number", "Period",
                                        "Media Client/Product", "Net Amount"]}
        self.total = {"TOTAL": []}

    def match(self, context: BlockSet) -> bool:
        status_list = []
        # check number match
        context = right(top(context, argument=40), 50)
        if TopRightCheckNumberChecker(anchor="CheckNo.").check(context):
            self.check_number = context

        # date number check

        return True

    def extract(self, context: BlockSet) -> List[Any]:
        extracted_params = {}

        return extracted_params
