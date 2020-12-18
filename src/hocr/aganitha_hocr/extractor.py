from typing import List, Dict, Any

from aganitha_hocr.matcher import Matcher
from aganitha_hocr.object_model import BlockSet
from aganitha_hocr.predicate import Predicate


class Extractor(object):

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

    def extract(self, context: BlockSet) -> Dict[str, Any]:
        pass
