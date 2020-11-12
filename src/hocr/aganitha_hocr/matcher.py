from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from typing import Optional, List, Union, Tuple, Any


class Matcher(object):

    def __init__(self, anchor: str, pattern: str):
        self.anchor = anchor
        self.pattern = pattern

    def match_rule(self, context: BlockSet) -> List[str]:
        pass
