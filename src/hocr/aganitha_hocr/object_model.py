# Imports
from typing import TypeVar, List, Optional
from aganitha_parsing_utils.html import HTMLParsingUtils
from fuzzywuzzy import fuzz
import logging
from src.hocr.aganitha_hocr.utils import Utils

logger = logging.getLogger(__name__)

# import collections

# TypeVars
Region_t = TypeVar('Region')
BlockSet_t = TypeVar('BlockSet')
Block_t = TypeVar('Block')
HOCRDoc_t = TypeVar('HOCRDoc')


class Region(object):
    """
    Region data structure defined by coordinates [x_top_left, y_top_left, x_bot_right, y_bot_right] on the parsed file.
    """

    def __init__(self, parent_doc: HTMLParsingUtils, x_top_left: int, y_top_left: int, x_bot_right: int, y_bot_right: int):
        self.parent_doc = parent_doc
        self.y_bot_right = y_bot_right
        self.x_bot_right = x_bot_right
        self.y_top_left = y_top_left
        self.x_top_left = x_top_left

    def get_parsed_values(self) -> object:
        """
        Objects are parsed sequentially in xpath. The function uses xpath matching to give
        title[A list of bbox] and word. Parsing is only done for class = 'ocrx_word'
        """
        # The bbox is sequentially listed
        title_list = Utils.split_bbox(self.parent_doc.match_xpath('.//span[@class="ocrx_word"]/@title'))
        text_list = self.parent_doc.match_xpath('.//span[@class="ocrx_word"]/text()')
        return title_list, text_list

    def get_blockset(self) -> BlockSet_t:
        """
        Returns all blocks as a BlockSet data structure present in the hocr file of class='ocrx_word'
        """
        bbox_list, word_list = self.get_parsed_values()
        x_top_left_coord = [t[0] for t in bbox_list]
        y_top_left_coord = [t[1] for t in bbox_list]
        x_bot_right_coord = [t[2] for t in bbox_list]
        y_bot_right_coord = [t[3] for t in bbox_list]
        blockset = []
        for i in range(0, len(word_list)):
            blockset.append(Block(self.parent_doc, x_top_left_coord[i], y_top_left_coord[i], x_bot_right_coord[i], y_bot_right_coord[i],
                                  word_list[i]))
        return BlockSet(blockset)

    def get_blockset_by_region(self) -> BlockSet_t:
        """
        Returns blocks as BlockSet data structure, but only for blocks inside the defined Region class.
        """
        bbox_list, word_list = self.get_parsed_values()
        x_top_left_coord = [t[0] for t in bbox_list]
        y_top_left_coord = [t[1] for t in bbox_list]
        x_bot_right_coord = [t[2] for t in bbox_list]
        y_bot_right_coord = [t[3] for t in bbox_list]
        blockset = []
        for i in range(0, len(word_list)):
            if (x_top_left_coord[i] > self.x_top_left) and (y_top_left_coord[i] > self.y_top_left) and \
                    (x_bot_right_coord[i] < self.x_bot_right) and (y_bot_right_coord[i] < self.y_bot_right):
                blockset.append(Block(self.parent_doc, x_top_left_coord[i], y_top_left_coord[i], x_bot_right_coord[i],
                                      y_bot_right_coord[i], word=word_list[i]))
        return BlockSet(blockset)


class BlockSet(object):
    """
    Behaviour should be as a list of blocks.
    You can use len(BlockSet) to find how many blocks are present.
    You can also use indexing like in a normal list.
    """

    def __init__(self, block_set: List[Block_t]):
        self.block_set = block_set

    def __len__(self):
        return len(self.block_set)

    def __getitem__(self, item):
        return self.block_set[item]


class Block(object):
    """
    Lowest level data structure. It is defined by the coordinates [x_top_left, y_top_left, x_bot_right, y_bot_right]
    and the word that is detected.
    """

    def __init__(self, parent_doc: HTMLParsingUtils, x_top_left: float, y_top_left: float, x_bot_right: float, y_bot_right: float, word: str):
        self.parent_doc = parent_doc
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.x_bot_right = x_bot_right
        self.y_bot_right = y_bot_right
        self.word = word
        self.x_centre = self.x_top_left + (self.x_bot_right - self.x_top_left)
        self.y_centre = self.y_top_left + (self.y_bot_right - self.y_top_left)


class HOCRDoc(object):

    def __init__(self, hocr_file: Optional[str]):
        self.hocr = HTMLParsingUtils(from_file=hocr_file)
        print(type(self.hocr))

    def parsed_object(self) -> HTMLParsingUtils:
        return self.hocr

    def find_region(self, query: str) -> Region:
        """
        The function takes a string query and understands it to define a Region data structure.
        :params query: str
        :return Region:
        Query parsed -> coordinates
        Region(coordinates)
        """
        query_obj = QueryCompiler(query)
        compiled_query = query_obj.compile()
        query_compile_obj = CompiledQuery(compiled_query)
        region = query_compile_obj.execute_query(self.hocr)
        return region

    def find_blockset_in_region(self, x_top_left: int, y_top_left: int, x_bot_right: int,
                                y_bot_right: int) -> BlockSet:
        """
        Given coordinates for a region, find the blockset.
        :params x_top_left: int, y_top_left: int, x_bot_right: int, y_bot_right: int:
        :returns BlockSet:
        """
        region = Region(self.hocr, x_top_left, y_top_left, x_bot_right, y_bot_right)
        blockset = region.get_blockset_by_region()

        return blockset

    @staticmethod
    def find_block_in_blockset(query: str, context: BlockSet):
        """
        Given a search query(A word) in context of a BlockSet find the required block.
        :param query: str
        :param context: BlockSet
        """
        for block in context:

            if fuzz.ratio(query, block.word) == 100:
                print('Perfect Match!')
                print('Query: ', query)
                print(' Block Word: ', block.word)
                print('Coordinates are [x_tl,y_tl,x_br, y_br]:', block.x_top_left, block.y_top_left,
                      block.x_bot_right,
                      block.y_bot_right)
                return

        print('No Match.')


# hocr = HOCRDoc('/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
# blocks = hocr.find_blockset_in_region(250, 300, 750, 750)
# hocr.find_block_in_blockset('KRAFT', blocks)
# hocr.find_block_in_blockset('KATZ', blocks)
"""
def main():
    hocr = HOCRDoc('/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
    blocks = hocr.find_blockset_in_region(250, 300, 750, 750)
    
    TOP:20
    [[TOP , 20], [BOT, 30]]
    Parse the above values
    Region (x,y)
    find_blockset_in_region(Region)
    
    
"""
"""
hocr = HTMLParsingUtils(from_file='/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
tmp = hocr.match_xpath('.//div[@class="ocr_page"]/@title')
print(tmp)
"""