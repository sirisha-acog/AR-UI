from src.hocr.aganitha_hocr.step import Step
from src.hocr.aganitha_hocr.query_engine import QueryCompiler, CompiledQuery
from src.hocr.aganitha_hocr.matched_template import MatchedTemplate
from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from typing import Optional, List, Union, Tuple
from aganitha_parsing_utils.html import HTMLParsingUtils


class Rule(object):
    """
    Matched template to be available
    Each rule should be able to refer input and outputs of previously computed rules
    """

    def __init__(self,anchor: str):
        self.anchor = anchor


    def check(self, context: BlockSet) -> bool:
        """
        It will take HOCRDoc or a blockset and check whether the anchor word exists at specified location
        """
        pass





