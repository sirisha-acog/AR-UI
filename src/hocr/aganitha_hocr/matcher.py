from aganitha_hocr.object_model import BlockSet, Block
from typing import Optional, List, Union, Tuple, Any


class Matcher(object):

    def __init__(self, anchor: Optional[str], pattern: Optional[str]):
        self.anchor = anchor
        self.pattern = pattern

    def match_rule(self, context: BlockSet) -> List[Any]:
        pass
