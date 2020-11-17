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

# MATCHERS -->

# OMG Class Extractor

class OMG(Extractor):

    def __init__(self):
        self.date: BlockSet = None
        self.check_number: BlockSet = None
        self.invoice_date: BlockSet = None
        self.invoice_number: BlockSet = None
        self.amount: BlockSet = None
        self.check_total: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        pass

    def extract(self, context:BlockSet) -> Dict:
        pass


