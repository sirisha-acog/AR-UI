from src.hocr.aganitha_hocr.step import Step
from src.hocr.aganitha_hocr.object_model import HOCRDoc
from typing import Optional, List
from aganitha_parsing_utils.html import HTMLParsingUtils
from src.hocr.aganitha_hocr.template import Template


class Rule(object):
    def __init__(self, query: List[str], assertion: List[str]):
        self.query = query
        self.assertion = assertion

    def validate(self, hocr_doc_obj: HTMLParsingUtils, state: Template) -> bool:
        """
        This function will take in hocr, run the query and perform assertion and return True
        if there is a template match.
        """

        pass
