from typing import List, Optional
from aganitha_parsing_utils.html import HTMLParsingUtils

from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.rule import Rule


class Template(object):
    def __init__(self, matched_rule: List[Rule]):
        self.matched_rules = matched_rule

    def match(self, context: BlockSet):
        pass

    def extract(self, context: BlockSet):
        pass

    def validate(self, context: BlockSet):
        pass

    def transform(self, context: BlockSet):
        pass
