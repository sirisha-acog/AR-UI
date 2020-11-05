#!/usr/bin/env python
# coding: utf-8

__author__ = "Abhishek Shakya"
__copyright__ = "2020 Aganitha Cognitive Solutions Private Limited"
__email__ = "abhishek.shakya@aganitha.ai"

"""
This file contains main code base.
"""

# importing libraries
# importing python modules


# importing third party libraries


# importing project dependencies
from src.hocr.aganitha_hocr.rule import import Rule
from src.hocr.aganitha_hocr.template import Template

class IPGTemplate(Template):
    def __init__(self):
        super().__init__(matched_rule=[TopRightDateRule()])

    def match(self, context: BlockSet):
        status = False
        for rule in self.matched_rule:
            if rule.check(context):
                return status

        status = True
        return status

    def extract(self, context: BlockSet):
        pass

    def validate(self, context: BlockSet):
        pass

    def transform(self, context: BlockSet):
        pass



class TopRightDateRule(Rule):

    def __init__(self):
        super(self).__init__(anchor="Date")

    def check(self, context:BlockSet) -> bool:
        context = top(context.get_block_from_blockset("Invoice"))
        context = bottom(context.get_block_from_blockset("Vendor ID"))
        if context.get_block_from_blockset(self.anchor):
            return True
        else
            return False