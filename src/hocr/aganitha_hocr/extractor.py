from typing import List, Dict, Any

from src.hocr.aganitha_hocr.matcher import Matcher
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.predicate import Predicate
from src.hocr.aganitha_hocr.utils import TemplateDidNotMatchError


class Extractor(object):

    def execute(self, context: BlockSet):
        if not self.match(context):
            raise TemplateDidNotMatchError()
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
