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

class 22SquaredTemplate(Template):
    def __init__(self):
        super().__init__()
        # list of rules
        self.matched_rule = [
            TopRightDateRule(query=[StepTop("top", "30"), StepRight("right", "20"), StepText("text", "Date")],
                             assertion='dd/MM/YYYY'),
            TopRightCheckNumberRule(
                query=[StepTop("top", "30"), StepRight("right", "20"), StepText("text", "Date")],
                assertion='dd/MM/YYYY'),
            ]

        # list of steps
        self.extraction_queries = [Nearest("Text", "Date")]


