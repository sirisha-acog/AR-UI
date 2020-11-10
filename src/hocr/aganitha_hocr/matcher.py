
from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from typing import Optional, List, Union, Tuple


class Matcher(object):
    def __init__(self, anchor:str):
        self.anchor = str

    def match_rule(self, context: BlockSet) -> List[str]:
        pass

