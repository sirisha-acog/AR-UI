from src.hocr.aganitha_hocr.object_model import Region
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.object_model import Block
from src.hocr.aganitha_hocr.object_model import HOCRDoc
from src.hocr.aganitha_hocr.utils import Utils
from typing import Union


class Step(object):
    def __init__(self, axis: str, argument: str):
        self.axis = axis
        self.argument = argument

    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        pass


class StepTop(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of top or 20% * page y value.
        return Region(x_top)
        """
        # if not context.parent_doc:
        # Takes from HOCRDoc instance attribute self.hocr as no region has been defined
        if isinstance(context, HOCRDoc):
            print("-----> Step applied on HOCRDoc Object")
            hocr = context.hocr
            title = hocr.match_xpath('.//div[@class="ocr_page"]/@title')
            # Get bbox coordinates
            bbox = Utils.split_bbox_page(title)
            # bbox = [x_top_left, y_top_left, x_bot_right, y_bot_right]
            arg = float(int(self.argument) * 0.01)
            return Region(parent_doc=hocr, x_top_left=bbox[0], y_top_left=bbox[1], x_bot_right=bbox[2],
                          y_bot_right=int(bbox[3] * arg))

        elif isinstance(context, Region):
            print("-----> Step applied on Region Object")
            parent_doc = context.parent_doc
            current_xtl = context.x_top_left
            current_ytl = context.y_top_left
            current_xbr = context.x_bot_right
            current_ybr = context.y_bot_right
            # arg to multiply with current_ybr
            arg = float(int(self.argument) * 0.01)
            return Region(parent_doc=parent_doc, x_top_left=current_xtl, y_top_left=current_ytl, x_bot_right=current_xbr
                          , y_bot_right=int(current_ybr * arg))


class StepBottom(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of bottom or 20% * page y value.
        return Region(x_bottom)
        """
        if isinstance(context, HOCRDoc):
            print("-----> Step applied on HOCRDoc Object")
            hocr = context.hocr
            title = hocr.match_xpath('.//div[@class="ocr_page"]/@title')
            # Get bbox coordinates
            bbox = Utils.split_bbox_page(title)
            # bbox = [x_top_left, y_top_left, x_bot_right, y_bot_right]
            arg = float(int(self.argument) * 0.01)
            new_y_top_left = bbox[3] - ((bbox[3] - bbox[1]) * arg)
            return Region(parent_doc=hocr, x_top_left=bbox[0], y_top_left=int(new_y_top_left), x_bot_right=bbox[2],
                          y_bot_right=bbox[3])

        elif isinstance(context, Region):
            print("-----> Step applied on Region Object")
            parent_doc = context.parent_doc
            current_xtl = context.x_top_left
            current_ytl = context.y_top_left
            current_xbr = context.x_bot_right
            current_ybr = context.y_bot_right
            # arg to multiply with current_ybr
            arg = float(int(self.argument) * 0.01)
            new_y_top_left = current_ybr - ((current_ybr - current_ytl) * arg)
            return Region(parent_doc=parent_doc, x_top_left=current_xtl, y_top_left=int(new_y_top_left),
                          x_bot_right=current_xbr
                          , y_bot_right=current_ybr)


class StepLeft(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of left or 20% * page x value.
        return Region(y_left)
        """
        if isinstance(context, HOCRDoc):
            print("-----> Step applied on HOCRDoc Object")
            hocr = context.hocr
            title = hocr.match_xpath('.//div[@class="ocr_page"]/@title')
            # Get bbox coordinates
            bbox = Utils.split_bbox_page(title)
            # bbox = [x_top_left, y_top_left, x_bot_right, y_bot_right]
            arg = float(int(self.argument) * 0.01)
            new_x_top_left = bbox[2] - ((bbox[2] - bbox[0]) * arg)
            return Region(parent_doc=hocr, x_top_left=int(new_x_top_left), y_top_left=bbox[1], x_bot_right=bbox[2],
                          y_bot_right=bbox[3])

        elif isinstance(context, Region):
            print("-----> Step applied on Region Object")
            parent_doc = context.parent_doc
            current_xtl = context.x_top_left
            current_ytl = context.y_top_left
            current_xbr = context.x_bot_right
            current_ybr = context.y_bot_right
            # arg to multiply with current_ybr
            arg = float(int(self.argument) * 0.01)
            new_x_top_left = current_xbr - ((current_xbr - current_xtl) * arg)
            return Region(parent_doc=parent_doc, x_top_left=int(new_x_top_left), y_top_left=current_ytl,
                          x_bot_right=current_xbr
                          , y_bot_right=current_ybr)


class StepRight(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get a new region >> 20% of right or 20% * page x value.
        return Region(x_bot_right)
        """
        if isinstance(context, HOCRDoc):
            print("-----> Step applied on HOCRDoc Object")
            hocr = context.hocr
            title = hocr.match_xpath('.//div[@class="ocr_page"]/@title')
            # Get bbox coordinates
            bbox = Utils.split_bbox_page(title)
            # bbox = [x_top_left, y_top_left, x_bot_right, y_bot_right]
            arg = float(int(self.argument) * 0.01)
            return Region(parent_doc=hocr, x_top_left=bbox[0], y_top_left=bbox[1], x_bot_right=int(bbox[2] * arg),
                          y_bot_right=bbox[3])

        elif isinstance(context, Region):
            print("-----> Step applied on Region Object")
            parent_doc = context.parent_doc
            current_xtl = context.x_top_left
            current_ytl = context.y_top_left
            current_xbr = context.x_bot_right
            current_ybr = context.y_bot_right
            # arg to multiply with current_ybr
            arg = float(int(self.argument) * 0.01)
            return Region(parent_doc=parent_doc, x_top_left=current_xtl, y_top_left=current_ytl,
                          x_bot_right=int(current_xbr * arg)
                          , y_bot_right=current_ybr)


class StepText(Step):
    def execute(self, context: Union[HOCRDoc, Region, Block]) -> Union[Region, BlockSet, Block]:
        """
        Get text from the region
        return Block
        """
        if isinstance(context, Region):
            blockset = context.get_blockset_by_region()
            HOCRDoc.find_block_in_blockset(self.argument, blockset)

        return context
