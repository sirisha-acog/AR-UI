from typing import List

from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from scipy.spatial.distance import euclidean


# TODO: Given a query containing multiple strings we should be able to identify block sets with some tolerance T.

def get_blocks_by_region(context: BlockSet, x_top_left: int, y_top_left: int,
                         x_bot_right: int, y_bot_right) -> List[Block]:
    block_list = []
    for block in context.blocks:
        if (block.x_top_left >= x_top_left) and (block.y_top_left >= y_top_left) and (block.x_bot_right <= x_bot_right) \
                and (block.y_bot_right <= y_bot_right):
            block_list.append(block)
    return block_list


def top(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    blocks = get_blocks_by_region(context, x_top_left=context.x_top_left,
                                  y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                                  y_bot_right=int(context.y_bot_right * argument * 0.01))

    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                    y_bot_right=int(context.y_bot_right * argument * 0.01), blocks=blocks)


def bot(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    new_y_top_left = context.y_bot_right - ((context.y_bot_right - context.y_top_left) * argument * 0.01)
    blocks = get_blocks_by_region(context, x_top_left=context.x_top_left,
                                  y_top_left=int(new_y_top_left), x_bot_right=context.x_bot_right,
                                  y_bot_right=context.y_bot_right)
    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=int(new_y_top_left), x_bot_right=context.x_bot_right,
                    y_bot_right=context.y_bot_right, blocks=blocks)


def right(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    new_x_top_left = context.x_bot_right - ((context.x_bot_right - context.x_top_left) * argument * 0.01)
    blocks = get_blocks_by_region(context, x_top_left=int(new_x_top_left),
                                  y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                                  y_bot_right=context.y_bot_right)
    return BlockSet(parent_doc=context.parent_doc, x_top_left=int(new_x_top_left),
                    y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                    y_bot_right=context.y_bot_right, blocks=blocks)


def left(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    blocks = get_blocks_by_region(context, x_top_left=context.x_top_left,
                                  y_top_left=context.y_top_left, x_bot_right=int(context.x_bot_right * argument * 0.01),
                                  y_bot_right=context.y_bot_right)
    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=context.y_top_left, x_bot_right=int(context.x_bot_right * argument * 0.01),
                    y_bot_right=context.y_bot_right, blocks=blocks)


def nearest(context: BlockSet, anchor: Block, axis: str) -> BlockSet:
    """
    Distance between centres should give use the nearest block
    """
    if axis.lower() == "right":
        right_coord_of_anchor = anchor.x_bot_right
        blocks = get_blocks_by_region(context, x_top_left=right_coord_of_anchor, y_top_left=context.y_top_left,
                                      x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                    default = block

        return BlockSet(parent_doc=context.parent_doc, blocks=[default])
    elif axis.lower() == "left":
        left_coord_of_anchor = anchor.x_top_left
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                                      x_bot_right=left_coord_of_anchor, y_bot_right=context.y_bot_right)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                    default = block

        return BlockSet(parent_doc=context.parent_doc, blocks=[default])
    elif axis.lower() == "top":
        top_coord_of_anchor = context.y_top_left
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                                      x_bot_right=context.x_bot_right, y_bot_right=top_coord_of_anchor)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                    default = block
    elif axis.lower() == "bot":
        bot_coord_of_anchor = context.y_bot_right
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=bot_coord_of_anchor,
                                      x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                    default = block
