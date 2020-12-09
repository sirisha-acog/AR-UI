#!/usr/bin/env python
# coding: utf-8
# importing project dependencies
from typing import Any, List, Dict

from aganitha_hocr.extractor import Extractor
from aganitha_hocr.filter import right, top, bot, left, nearest, get_text, \
    get_blockset_by_anchor_axis, intersection, nearest_block_with_delta
from aganitha_hocr.object_model import BlockSet
from aganitha_hocr.predicate import Predicate
from aganitha_hocr.matcher import Matcher
import re
import logging

logger = logging.getLogger(__name__)


# MATCHERS-->
class IndiaMatcher(Matcher):
    def match_rule(self, context: BlockSet) -> List[str]:
        india_blockset = get_text(context, named_params={"query": "EU", "level": "word"})
        col_ref = get_text(context, named_params={"query": "Novavax", "level": "word"})
        # print(india_blockset.get_synthetic_block().__dict__)
        nearest_block_with_delta(context, named_params={"row reference": india_blockset.get_synthetic_block(),
                                                        "col reference": col_ref.get_synthetic_block(),
                                                        "axis": "right", "delta_y": 0.5, "delta_x": 0.05})


class OtherDoc(Extractor):
    def __init__(self):
        self.india: BlockSet = None
        self.novavax: BlockSet = None

    def match(self, context: BlockSet) -> bool:
        self.india = top(context, named_params={"argument": 40})
        return True

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        extracted_params = {}
        value = IndiaMatcher(anchor="India", pattern=" ").match_rule(self.india)
        return extracted_params
