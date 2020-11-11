from typing import List, Union

from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from scipy.spatial.distance import euclidean
import logging

logger = logging.getLogger(__name__)


# TODO: 1. Given a query containing multiple strings, we should be able to identify block sets with some tolerance T.
# TODO: 2. Given a query containing multiple strings, we should be able to return union or intersection of all blocksets
# TODO: 3. Given a pattern in nearest filter, we should be able to get blockset matching the pattern

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


def nearest(context: BlockSet, anchor: Union[Block, BlockSet], axis: str) -> BlockSet:
    """
    Distance between centres should give use the nearest block
    """
    if axis.lower() == "right":
        right_coord_of_anchor = anchor.x_bot_right
        blocks = get_blocks_by_region(context, x_top_left=right_coord_of_anchor, y_top_left=context.y_top_left,
                                      x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right)
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([block.x_top_left, ((block.y_bot_right - block.y_top_left)/2) + block.y_top_left],
                             [anchor.x_bot_right, ((anchor.y_bot_right - anchor.y_top_left)/2) + anchor.y_top_left]) < min_dist:
                    min_dist = euclidean([block.x_top_left, ((block.y_bot_right - block.y_top_left)/2) + block.y_top_left],
                             [anchor.x_bot_right, ((anchor.y_bot_right - anchor.y_top_left)/2) + anchor.y_top_left])
                    default = block
                    # print("Block: ", default.word, " Current Dist: ", euclidean([block.x_top_left, (block.y_bot_right-block.y_top_left)/2], [anchor.x_bot_right, (anchor.y_bot_right - anchor.y_top_left)/2]) ," Distance: ", min_dist)
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])

    elif axis.lower() == "left":
        left_coord_of_anchor = anchor.x_top_left
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                                      x_bot_right=left_coord_of_anchor, y_bot_right=context.y_bot_right)
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([block.x_bot_right, ((block.y_bot_right - block.y_top_left)/2) + block.y_top_left],
                             [anchor.x_top_left, ((anchor.y_bot_right - anchor.y_top_left)/2) + anchor.y_top_left]) < min_dist:
                    min_dist = euclidean([block.x_bot_right, ((block.y_bot_right - block.y_top_left)/2) + block.y_top_left],
                             [anchor.x_top_left, ((anchor.y_bot_right - anchor.y_top_left)/2) + anchor.y_top_left])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])

    elif axis.lower() == "top":
        top_coord_of_anchor = anchor.y_top_left
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                                      x_bot_right=context.x_bot_right, y_bot_right=top_coord_of_anchor)
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([((block.x_bot_right-block.x_top_left)/2) + block.x_top_left, block.y_bot_right],
                             [((anchor.x_bot_right - anchor.x_top_left)/2) + anchor.x_top_left, anchor.y_top_left]) < min_dist:
                    min_dist = euclidean([((block.x_bot_right-block.x_top_left)/2) + block.x_top_left, block.y_bot_right],
                                         [((anchor.x_bot_right - anchor.x_top_left)/2) + anchor.x_top_left, anchor.y_top_left])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])

    elif axis.lower() == "bot":
        bot_coord_of_anchor = anchor.y_bot_right
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=bot_coord_of_anchor,
                                      x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right)
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_top_left],
                             [((anchor.x_bot_right - anchor.x_top_left) / 2) + anchor.x_top_left,
                              anchor.y_bot_right]) < min_dist:
                    min_dist = euclidean([((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_top_left],
                             [((anchor.x_bot_right - anchor.x_top_left) / 2) + anchor.x_top_left,
                              anchor.y_bot_right])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])


# TODO Modify nearest_by_text() according to original nearest logic
def nearest_by_text(context: BlockSet, anchor: Union[Block, BlockSet], query: str, axis: str) -> BlockSet:
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
                if query == block.word:
                    default = block
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
                if query == block.word:
                    default = block
                    if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])

    elif axis.lower() == "top":
        top_coord_of_anchor = anchor.y_top_left
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                                      x_bot_right=context.x_bot_right, y_bot_right=top_coord_of_anchor)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if query == block.word:
                    default = block
                    if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])

    elif axis.lower() == "bot":
        bot_coord_of_anchor = anchor.y_bot_right
        blocks = get_blocks_by_region(context, x_top_left=context.x_top_left, y_top_left=bot_coord_of_anchor,
                                      x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right)
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if query == block.word:
                    default = block
                    if euclidean(block.centre, anchor.centre) < euclidean(default.centre, anchor.centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, blocks=[default])


def get_text(context: BlockSet, query: str, level: str = "word") -> Union[BlockSet, List[Block]]:
    """
    Take input = [Paid, on, behalf, of]
    Want to bundle them together in a blockset.
    So when user does get_text(context, "Paid on behalf of") we get this
    blockset and use it as an input to nearest function.
    nearest(context, get_text(context, "Paid on behalf of"), axis = right) we get
    Martin as answer

    Define a BlockSet function where it "sets" the BlockSet x,y coordinates based
    on the coordinates of blocks it encompasses

    first search for all the words in the given query.
    2 conditions, 1 for single length query and another for multi length query
    for text in query:
        find nearest block to the text in right and bottom directions
            if the block.word is text.next
            append the block to a blockset and return a new blockset.
    """
    if level == "word":
        return context.get_blockset_by_query(query)
    elif level == "phrase":
        # Check if All the queries are present
        query = query.split()
        status = True
        query_list = []
        for text in query:
            if not context.get_blockset_by_query(text):
                status = False
                logger.debug("%r is not present in context. Status = %r", text, status)
            query_list.append(context.get_blockset_by_query(text))
        logger.debug("Ran Successfully. Status = %r", status)
        base = query_list[0]
        base = base.blocks[0]
        block_set = [base]
        for i in range(0, (len(query_list) - 1)):
            anchor_block_set = query_list[i]
            next_right = nearest_by_text(context, anchor_block_set.blocks[0], query=query_list[i + 1].blocks[0].word,
                                         axis="right")
            next_bot = nearest_by_text(context, anchor_block_set.blocks[0], query=query_list[i + 1].blocks[0].word,
                                       axis="bot")
            logger.debug("Next Right: %r", next_right.blocks[0].word)
            logger.debug("Next Bot: %r", next_bot.blocks[0].word)
            block_set.append(next_right.blocks[0])
        return block_set


def union(context1: BlockSet, context2: BlockSet) -> BlockSet:
    """
    choose max xtl,ytl,xbr,ybr and update total blocks = [context1.blocks + context2.blocks]
    """
    new_x_top_left = min(context1.x_top_left, context2.x_top_left)
    new_y_top_left = min(context1.y_top_left, context2.y_top_left)
    new_x_bot_right = max(context1.x_bot_right, context2.x_bot_right)
    new_y_bot_right = max(context1.y_bot_right, context2.y_bot_right)
    blocks = context1.blocks + context2.blocks
    return BlockSet(parent_doc=context1.parent_doc, x_top_left=new_x_top_left, y_top_left=new_y_top_left,
                    x_bot_right=new_x_bot_right,
                    y_bot_right=new_y_bot_right, blocks=blocks)


def intersection(context1: BlockSet, context2: BlockSet) -> BlockSet:
    """
    doOverlap? -> bool:
        if yes:
            we want coordinates of intersection rectangle. find all blocks in that rectangle by
            get_blocks_by_region(context = context1, coords = [intersection_rectangel_coords])
            return BlockSet withr elevant blocks

    """
    # If one rectangle is on left side of other
    if context1.x_top_left >= context2.x_bot_right or context2.x_top_left >= context1.x_bot_right:
        logger.debug("DOES NOT INTERSECT")
    # If one rectangle is above other
    elif context1.y_top_left <= context2.y_bot_right or context2.y_top_left <= context1.y_bot_right:
        logger.debug("DOES NOT INTERSECT")
    else:
        # Look up https://math.stackexchange.com/a/2477358 for logic
        logger.debug("Blocks Do Intersect")
        new_x_top_left = max(context1.x_top_left, context2.x_top_left)
        new_y_top_left = max(context1.y_top_left, context2.y_top_left)
        new_x_bot_right = min(context1.x_bot_right, context2.x_bot_right)
        new_y_bot_right = min(context1.y_bot_right, context2.y_bot_right)
        blocks = get_blocks_by_region(context=context1, x_top_left=new_x_top_left, y_top_left=new_y_top_left,
                                      x_bot_right=new_x_bot_right, y_bot_right=new_y_bot_right)
        return BlockSet(parent_doc=context1.parent_doc, x_top_left=new_x_top_left, y_top_left=new_y_top_left,
                        x_bot_right=new_x_bot_right,
                        y_bot_right=new_y_bot_right, blocks=blocks)
