from src.hocr.aganitha_hocr.object_model import Region
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.object_model import Block
from src.hocr.aganitha_hocr.object_model import HOCRDoc

from typing import Union


class Step(object):
    def __init__(self, axis: str, argument: str):
        self.axis = axis
        # ToDO: Parsing percentage from argument
        self.argument = argument

    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        pass


class StepTop(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of top or 20% * page y value.
        return Region(x_top)
        """
        if not context.parent_doc:
            hocr = context.hocr
        else:
            hocr = context.parent_doc

        return


class StepBottom(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of bottom or 20% * page y value.
        return Region(x_bottom)
        """
        return


class StepLeft(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of left or 20% * page x value.
        return Region(y_left)
        """
        return


class StepRight(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of right or 20% * page x value.
        return Region(y_right)
        """
        return


class StepText(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get text from the region
        return Block
        """
        return
