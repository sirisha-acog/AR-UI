from typing import List, Dict

from src.hocr.aganitha_hocr.object_model import BlockSet, Block
from scipy.spatial.distance import euclidean
import logging
import re
import pandas as pd
import shapely
from shapely.geometry import box
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

logger = logging.getLogger(__name__)


# TODO: 3. Given a query containing multiple strings, we should be able to identify block sets with some tolerance T.

def get_blocks_by_region(context: BlockSet, named_params: Dict) -> BlockSet:
    block_list = []
    for block in context.blocks:
        if (block.x_top_left > named_params['x_top_left']) and (block.y_top_left > named_params['y_top_left']) and (
                block.x_bot_right <= named_params['x_bot_right']) \
                and (block.y_bot_right <= named_params['y_bot_right']):
            block_list.append(block)
    return BlockSet(parent_doc=context.parent_doc, blocks=block_list)


def top(context: BlockSet, named_params: Dict) -> BlockSet:
    block_set = get_blocks_by_region(context, named_params={'x_top_left': context.x_top_left,
                                                            'y_top_left': context.y_top_left,
                                                            'x_bot_right': context.x_bot_right,
                                                            'y_bot_right': int(
                                                                context.y_bot_right * named_params['argument'] * 0.01)})

    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                    y_bot_right=int(context.y_bot_right * named_params['argument'] * 0.01), blocks=block_set.blocks)


def bot(context: BlockSet, named_params: Dict) -> BlockSet:
    new_y_top_left = context.y_bot_right - (
            (context.y_bot_right - context.y_top_left) * named_params['argument'] * 0.01)
    block_set = get_blocks_by_region(context, named_params={'x_top_left': context.x_top_left,
                                                            'y_top_left': int(new_y_top_left),
                                                            'x_bot_right': context.x_bot_right,
                                                            'y_bot_right': context.y_bot_right})
    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=int(new_y_top_left), x_bot_right=context.x_bot_right,
                    y_bot_right=context.y_bot_right, blocks=block_set.blocks)


def right(context: BlockSet, named_params: Dict) -> BlockSet:
    new_x_top_left = context.x_bot_right - (
            (context.x_bot_right - context.x_top_left) * named_params['argument'] * 0.01)
    block_set = get_blocks_by_region(context, named_params={'x_top_left': int(new_x_top_left),
                                                            'y_top_left': context.y_top_left,
                                                            'x_bot_right': context.x_bot_right,
                                                            'y_bot_right': context.y_bot_right})
    return BlockSet(parent_doc=context.parent_doc, x_top_left=int(new_x_top_left),
                    y_top_left=context.y_top_left, x_bot_right=context.x_bot_right,
                    y_bot_right=context.y_bot_right, blocks=block_set.blocks)


def left(context: BlockSet, named_params: Dict) -> BlockSet:
    block_set = get_blocks_by_region(context, named_params={'x_top_left': context.x_top_left,
                                                            'y_top_left': context.y_top_left,
                                                            'x_bot_right': int(
                                                                context.x_bot_right * named_params['argument'] * 0.01),
                                                            'y_bot_right': context.y_bot_right})
    return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left,
                    y_top_left=context.y_top_left,
                    x_bot_right=int(context.x_bot_right * named_params['argument'] * 0.01),
                    y_bot_right=context.y_bot_right, blocks=block_set.blocks)


def nearest(context: BlockSet, named_params: Dict) -> BlockSet:
    """
    Distance between edges should give use the nearest block
    """
    if named_params['axis'].lower() == "right":
        right_coord_of_anchor = named_params['anchor'].x_bot_right
        blocks = get_blocks_by_region(context, named_params={'x_top_left': right_coord_of_anchor,
                                                             'y_top_left': context.y_top_left,
                                                             'x_bot_right': context.x_bot_right,
                                                             'y_bot_right': context.y_bot_right})
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([block.x_top_left, ((block.y_bot_right - block.y_top_left) / 2) + block.y_top_left],
                             [named_params['anchor'].x_bot_right,
                              ((named_params['anchor'].y_bot_right - named_params['anchor'].y_top_left) / 2) +
                              named_params['anchor'].y_top_left]) < min_dist:
                    min_dist = euclidean(
                        [block.x_top_left, ((block.y_bot_right - block.y_top_left) / 2) + block.y_top_left],
                        [named_params['anchor'].x_bot_right,
                         ((named_params['anchor'].y_bot_right - named_params['anchor'].y_top_left) / 2) + named_params[
                             'anchor'].y_top_left])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "left":
        left_coord_of_anchor = named_params['anchor'].x_top_left
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left, 'y_top_left': context.y_top_left,
                                                    'x_bot_right': left_coord_of_anchor,
                                                    'y_bot_right': context.y_bot_right})
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([block.x_bot_right, ((block.y_bot_right - block.y_top_left) / 2) + block.y_top_left],
                             [named_params['anchor'].x_top_left,
                              ((named_params['anchor'].y_bot_right - named_params['anchor'].y_top_left) / 2) +
                              named_params['anchor'].y_top_left]) < min_dist:
                    min_dist = euclidean(
                        [block.x_bot_right, ((block.y_bot_right - block.y_top_left) / 2) + block.y_top_left],
                        [named_params['anchor'].x_top_left,
                         ((named_params['anchor'].y_bot_right - named_params['anchor'].y_top_left) / 2) + named_params[
                             'anchor'].y_top_left])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "top":
        top_coord_of_anchor = named_params['anchor'].y_top_left
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left,
                                                    'y_top_left': context.y_top_left,
                                                    'x_bot_right': context.x_bot_right,
                                                    'y_bot_right': top_coord_of_anchor})
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_bot_right],
                             [((named_params['anchor'].x_bot_right - named_params['anchor'].x_top_left) / 2) +
                              named_params['anchor'].x_top_left,
                              named_params['anchor'].y_top_left]) < min_dist:
                    min_dist = euclidean(
                        [((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_bot_right],
                        [((named_params['anchor'].x_bot_right - named_params['anchor'].x_top_left) / 2) + named_params[
                            'anchor'].x_top_left, named_params['anchor'].y_top_left])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "bot":
        bot_coord_of_anchor = named_params['anchor'].y_bot_right
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left,
                                                    'y_top_left': bot_coord_of_anchor,
                                                    'x_bot_right': context.x_bot_right,
                                                    'y_bot_right': context.y_bot_right})
        default = None
        min_dist = float('inf')
        if len(blocks) != 0:
            for block in blocks:
                if euclidean([((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_top_left],
                             [((named_params['anchor'].x_bot_right - named_params['anchor'].x_top_left) / 2) +
                              named_params['anchor'].x_top_left,
                              named_params['anchor'].y_bot_right]) < min_dist:
                    min_dist = euclidean(
                        [((block.x_bot_right - block.x_top_left) / 2) + block.x_top_left, block.y_top_left],
                        [((named_params['anchor'].x_bot_right - named_params['anchor'].x_top_left) / 2) + named_params[
                            'anchor'].x_top_left,
                         named_params['anchor'].y_bot_right])
                    default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])


def nearest_by_query(context: BlockSet, named_params: Dict) -> BlockSet:
    """
    Distance between centres should give use the nearest block
    """
    if named_params['axis'].lower() == "right":
        right_coord_of_anchor = named_params['anchor'].x_bot_right
        blocks = get_blocks_by_region(context, named_params={'x_top_left': right_coord_of_anchor,
                                                             'y_top_left': context.y_top_left,
                                                             'x_bot_right': context.x_bot_right,
                                                             'y_bot_right': context.y_bot_right})

        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if re.search(re.escape(named_params['pattern']), block.word):
                    default = block
                    if euclidean(block.centre, named_params['anchor'].centre) < euclidean(default.centre,
                                                                                          named_params[
                                                                                              'anchor'].centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "left":
        left_coord_of_anchor = named_params['anchor'].x_top_left
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left,
                                                    'y_top_left': context.y_top_left,
                                                    'x_bot_right': left_coord_of_anchor,
                                                    'y_bot_right': context.y_bot_right})
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if re.search(re.escape(named_params['pattern']), block.word):
                    default = block
                    if euclidean(block.centre, named_params['anchor'].centre) < euclidean(default.centre,
                                                                                          named_params[
                                                                                              'anchor'].centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "top":
        top_coord_of_anchor = named_params['anchor'].y_top_left
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left,
                                                    'y_top_left': context.y_top_left,
                                                    'x_bot_right': context.x_bot_right,
                                                    'y_bot_right': top_coord_of_anchor})
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if re.search(re.escape(named_params['pattern']), block.word):
                    default = block
                    if euclidean(block.centre, named_params['anchor'].centre) < euclidean(default.centre,
                                                                                          named_params[
                                                                                              'anchor'].centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])

    elif named_params['axis'].lower() == "bot":
        bot_coord_of_anchor = named_params['anchor'].y_bot_right
        blocks = get_blocks_by_region(context,
                                      named_params={'x_top_left': context.x_top_left,
                                                    'y_top_left': bot_coord_of_anchor,
                                                    'x_bot_right': context.x_bot_right,
                                                    'y_bot_right': context.y_bot_right})
        default = blocks[0]
        if len(blocks) != 0:
            for block in blocks:
                if re.search(re.escape(named_params['pattern']), block.word):
                    default = block
                    if euclidean(block.centre, named_params['anchor'].centre) < euclidean(default.centre,
                                                                                          named_params[
                                                                                              'anchor'].centre):
                        default = block
        return BlockSet(parent_doc=context.parent_doc, x_top_left=default.x_top_left, y_top_left=default.y_top_left,
                        x_bot_right=default.x_bot_right, y_bot_right=default.y_bot_right, blocks=[default])


def get_text(context: BlockSet, named_params: Dict) -> BlockSet:
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
    if named_params['level'] == "word":
        return context.get_blockset_by_query(named_params['query'])
    elif named_params['level'] == "phrase":
        # Check if All the queries are present
        query = named_params['query'].split()
        status = True
        query_list = []
        for text in query:
            if not context.get_blockset_by_query(text):
                status = False
                logger.debug("%r is not present in context. Status = %r", text, status)
            query_list.append(context.get_blockset_by_query(text))
        if status:
            logger.debug("Ran Successfully. Status = %r", status)
            base = query_list[0]
            base = base.blocks[0]
            block_set = [base]
            for i in range(0, (len(query_list) - 1)):
                anchor_block_set = query_list[i]
                next_right = nearest_by_query(context, named_params={'anchor': anchor_block_set.blocks[0],
                                                                     'pattern': query_list[i + 1].blocks[0].word,
                                                                     'axis': "right"})
                next_bot = nearest_by_query(context, named_params={'anchor': anchor_block_set.blocks[0],
                                                                   'pattern': query_list[i + 1].blocks[0].word,
                                                                   'axis': "bot"})
                logger.debug("Next Right: %r", next_right.blocks[0].word)
                logger.debug("Next Bot: %r", next_bot.blocks[0].word)
                if next_right.blocks[0].word == query_list[i + 1].blocks[0].word:
                    block_set.append(next_right.blocks[0])
                if next_bot.blocks[0].word == query_list[i + 1].blocks[0].word and \
                        next_right.blocks[0].word != query_list[i + 1].blocks[0].word:
                    block_set.append(next_bot.blocks[0])
        else:
            block_set = []

        return BlockSet(parent_doc=context.parent_doc, blocks=block_set)


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
            get_blocks_by_region(context = context1, coords = [intersection_rectangle_coords])
            return BlockSet with relevant blocks

    """
    # context1_polygon = box(context1.x_top_left, context1.y_top_left, context1.x_bot_right, context1.y_bot_right)
    # context2_polygon = box(context2.x_top_left, context2.y_top_left, context2.x_bot_right, context2.y_bot_right)
    # If one rectangle is on left side of other
    if context1.x_top_left >= context2.x_bot_right or context2.x_top_left >= context1.x_bot_right:
        logger.debug("DOES NOT INTERSECT")
    # If one rectangle is above other
    elif context1.y_top_left >= context2.y_bot_right or context2.y_top_left >= context1.y_bot_right:
        logger.debug("DOES NOT INTERSECT")
    else:
        # Look up https://math.stackexchange.com/a/2477358 for logic
        logger.debug("Blocks Intersect")
        new_x_top_left = max(context1.x_top_left, context2.x_top_left)
        new_y_top_left = max(context1.y_top_left, context2.y_top_left)
        new_x_bot_right = min(context1.x_bot_right, context2.x_bot_right)
        new_y_bot_right = min(context1.y_bot_right, context2.y_bot_right)
        block_set = get_blocks_by_region(context=context1,
                                         named_params={'x_top_left': new_x_top_left,
                                                       'y_top_left': new_y_top_left,
                                                       'x_bot_right': new_x_bot_right,
                                                       'y_bot_right': new_y_bot_right})
        return BlockSet(parent_doc=context1.parent_doc, x_top_left=new_x_top_left, y_top_left=new_y_top_left,
                        x_bot_right=new_x_bot_right,
                        y_bot_right=new_y_bot_right, blocks=block_set.blocks)


def loose_intersection(context1: BlockSet, context2: BlockSet, named_params: Dict) -> BlockSet:
    """
    It take two blocksets and returns blockset if there are any blocks inside the overlapping region.
    The block need not be entirely inside overlapping region. The overlapping threshold need to be
    passed while calling the filter
    """

    context1_polygon = box(context1.x_top_left, context1.y_top_left, context1.x_bot_right, context1.y_bot_right)
    context2_polygon = box(context2.x_top_left, context2.y_top_left, context2.x_bot_right, context2.y_bot_right)
    overlap_polygon_status = context1_polygon.intersects(context2_polygon)
    if overlap_polygon_status:
        overlap_polygon = box(*context1_polygon.intersection(context2_polygon).bounds)
        block_df = pd.DataFrame(columns=['block', 'overlap area'])
        for block in set(context1.blocks + context2.blocks):
            block_polygon = box(block.x_top_left, block.y_top_left, block.x_bot_right, block.y_bot_right)
            overlap_area = overlap_polygon.intersection(block_polygon).area
            if block_polygon.area > 0 and overlap_area > 0:
                percentage_overlap_area = 100 * overlap_area / block_polygon.area
                if percentage_overlap_area > named_params['threshold']:
                    block_dict = {'block': block, 'overlap area': percentage_overlap_area}
                    block_df = block_df.append(block_dict, ignore_index=True)

        block_df = block_df.sort_values(by='overlap area', ascending=False)
        block_list = list(block_df['block'])

        return BlockSet(parent_doc=context1.parent_doc, blocks=block_list)
    else:
        logger.debug('DOES NOT INERSECT')
        return BlockSet(parent_doc=context1.parent_doc, blocks=[])


def get_blockset_by_anchor_axis(context: BlockSet, named_params: Dict) -> BlockSet:
    """

    """
    if named_params['axis'].lower() == "right":
        right_coord_of_anchor = named_params['anchor'].x_bot_right
        block_set = get_blocks_by_region(context, named_params={'x_top_left': right_coord_of_anchor,
                                                                'y_top_left': context.y_top_left,
                                                                'x_bot_right': context.x_bot_right,
                                                                'y_bot_right': context.y_bot_right})
        return BlockSet(parent_doc=context.parent_doc, x_top_left=right_coord_of_anchor, y_top_left=context.y_top_left,
                        x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right, blocks=block_set.blocks)

    elif named_params['axis'].lower() == "left":
        left_coord_of_anchor = named_params['anchor'].x_top_left
        block_set = get_blocks_by_region(context,
                                         named_params={'x_top_left': context.x_top_left,
                                                       'y_top_left': context.y_top_left,
                                                       'x_bot_right': left_coord_of_anchor,
                                                       'y_bot_right': context.y_bot_right})

        return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                        x_bot_right=left_coord_of_anchor, y_bot_right=context.y_bot_right, blocks=block_set.blocks)

    elif named_params['axis'].lower() == "top":
        top_coord_of_anchor = named_params['anchor'].y_top_left
        block_set = get_blocks_by_region(context,
                                         named_params={'x_top_left': context.x_top_left,
                                                       'y_top_left': context.y_top_left,
                                                       'x_bot_right': context.x_bot_right,
                                                       'y_bot_right': top_coord_of_anchor})
        return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left, y_top_left=context.y_top_left,
                        x_bot_right=context.x_bot_right, y_bot_right=top_coord_of_anchor, blocks=block_set.blocks)

    elif named_params['axis'].lower() == "bot":
        bot_coord_of_anchor = named_params['anchor'].y_bot_right
        block_set = get_blocks_by_region(context,
                                         named_params={'x_top_left': context.x_top_left,
                                                       'y_top_left': bot_coord_of_anchor,
                                                       'x_bot_right': context.x_bot_right,
                                                       'y_bot_right': context.y_bot_right})

        return BlockSet(parent_doc=context.parent_doc, x_top_left=context.x_top_left, y_top_left=bot_coord_of_anchor,
                        x_bot_right=context.x_bot_right, y_bot_right=context.y_bot_right, blocks=block_set.blocks)


def nearest_block_with_delta(context: BlockSet, named_params: Dict):
    """
    test
    named_params["row reference"] -> Block
    named_params["column reference"] ->  Block
    named_params["axis"] -> str
    named_params["delta_x"] -> float
    named_params["delta_y"] -> float
    """
    ytl_ref = named_params["row reference"].y_top_left
    ybr_ref = named_params["row reference"].y_bot_right
    xtl_ref = named_params["col reference"].x_top_left
    xbr_ref = named_params["col reference"].x_bot_right
    # print(named_params)
    # print(ytl_ref, ybr_ref)
    delta_y = float(named_params["delta_y"])
    delta_x = float(named_params["delta_x"])
    # print(delta)
    if named_params['axis'] == "right":
        # print(" Inside If")
        for block in context.blocks:
            # print(block.word, block.y_top_left, block.y_bot_right)
            if (ytl_ref * (1 - delta_x) <= float(block.y_top_left) <= ytl_ref * (1 + delta_x)) or (
                    ybr_ref * (1 - delta_x) <= float(block.y_bot_right) <= ybr_ref * (1 + delta_x)):
                # print("Inside If")
                if (xtl_ref * (1 - delta_y) <= float(block.x_top_left) <= xtl_ref * (1 + delta_y)) or (
                        xbr_ref * (1 - delta_y) <= float(block.x_bot_right) <= xbr_ref * (1 + delta_y)):
                    print(block.word)
