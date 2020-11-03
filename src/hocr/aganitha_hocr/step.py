from src.hocr.aganitha_hocr.object_model import Region
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.object_model import Block


from typing import Union


class Step(object):
    def __init__(self, axis: str, argument: str):
        self.axis = axis
        # Parsing percentage
        self.argument = argument

    def execute(self, context: Region) -> Union[Region, BlockSet, Block]:
        pass


class StepTOP(Step):
    def execute(self, context: Region) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of top or 20% * page y value.
        return Region(x_top)
        """
        return