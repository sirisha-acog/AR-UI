from typing import List, Optional
from aganitha_parsing_utils.html import HTMLParsingUtils

from src.hocr.aganitha_hocr.matched_template import MatchedTemplate
from src.hocr.aganitha_hocr.rule import Rule


class Template(object):
    def __init__(self, matched_rule: List[Rule], extraction_queries: List[str]):
        self.matched_rule = matched_rule
        self.extraction_queries = extraction_queries

    def match(self, doc: HTMLParsingUtils, state: Optional[MatchedTemplate, None]):
        pass
