from typing import List, Any

from src.hocr.aganitha_hocr.matcher import Matcher
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate


class Extractor(object):
    def __init__(self, matched_list: List[Matcher], predicate_list: List[Predicate]):
        self.matched_list = matched_list
        self.predicate_list = predicate_list

    def execute(self, context: BlockSet):
        if not self.match(context):
            raise Exception
        else:
            extracted_data = self.extract(context)

        return extracted_data

    def match(self, context: BlockSet) -> bool:
        """
        for matcher in List[Matchers]:
            do_something
        """
        pass

    def extract(self, context: BlockSet) -> List[str]:
        pass
