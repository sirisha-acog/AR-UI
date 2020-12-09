from aganitha_hocr.object_model import BlockSet
from typing import Dict


class Predicate(object):
    def __init__(self, anchor: str):
        self.anchor = anchor

    def check(self, context: BlockSet) -> bool:
        pass
