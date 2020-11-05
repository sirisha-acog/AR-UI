#!/usr/bin/env python
# coding: utf-8

__author__ = "Abhishek Shakya"
__copyright__ = "2020 Aganitha Cognitive Solutions Private Limited"
__email__ = "abhishek.shakya@aganitha.ai"

"""
This file contains template info for customer - MMS.
"""

# importing libraries
# importing python modules


# importing third party libraries


# importing project dependencies
from src.hocr.aganitha_hocr.template import Template
from src.hocr.aganitha_hocr.matched_template import MatchedTemplate
from src.hocr.aganitha_hocr.rule import TopRightDateRule, TopLeftCustomerNameRule


class MMS(Template):

    def __init__(self):
        self.matched_rule.extend(TopRightDateRule(), TopLeftCustomerNameRule())


    def match(doc: HOCRDoc) -> MatchedTemplate:
        matched_template = MatchedTemplate()
        for r in matching_rules:
            assert r.validate(hocr_doc, matched_template) == True
