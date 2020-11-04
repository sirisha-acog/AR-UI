from src.hocr.aganitha_hocr.step import Step
from src.hocr.aganitha_hocr.object_model import HOCRDoc
from typing import Optional, List
from aganitha_parsing_utils.html import HTMLParsingUtils


class Rule(object):
    """
    Matched template to be available
    Each rule should be able to refer input and outputs of previously computed rules
    """
    def __init__(self, query: List[str], assertion: List[str]):
        self.query = query
        self.assertion = assertion


    def validate(self, hocr_doc: HTMLParsingUtils) -> bool:
        """
        This function will take in hocr, run the query and perform assertion and return True
        if there is a template match.
        """

        pass


class TopRightDateRule(Rule):
    """
    This rule checks if there is a Date in the top right corner of the page
    """
    def validate(self, hocr_doc: HTMLParsingUtils) -> bool:
        pass


class TopRightCheckNumberRule(Rule):
    """
    This rule checks if there is a Check number in the top right corner of the page
    """
    def validate(self, hocr_doc: HTMLParsingUtils) -> bool:
        pass


class TopRightVendorIdRule(Rule):
    """
    This rule checks if there is a Vendor Id in the top right corner of the page
    """
    def validate(self, hocr_doc: HTMLParsingUtils) -> bool:
        pass


class TopLeftCustomerNameRule(Rule):
    """
    This rule checks if there is a Customer name in the top left corner of the page
    """
    def validate(self, hocr_doc: HTMLParsingUtils) -> bool:
        pass


class TableHeadersRule(Rule):
    """
    This rule checks for table headers in the block or blockset
    """
    def validate(self, hocr_doc: HTMLParsingUtils):
        pass