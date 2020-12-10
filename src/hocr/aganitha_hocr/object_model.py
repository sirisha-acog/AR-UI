# Imports
from typing import TypeVar, List, Optional, Union
from aganitha_parsing_utils.html import HTMLParsingUtils
from fuzzywuzzy import fuzz
import logging
from aganitha_hocr.utils import Utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# import collections

# TypeVars
BlockSet_t = TypeVar('BlockSet')
Block_t = TypeVar('Block')
Page_t = TypeVar('Page')


class BlockSet(object):
    """
    Behaviour should be as a list of blocks. in a region defined by the [x_top_left, y_top_left,
    x_bot_right, y_bot_right].
    You can use len(BlockSet) to find how many blocks are present.
    You can also use indexing like in a normal list.
    """

    def __init__(self, parent_doc: HTMLParsingUtils, blocks: List[Block_t], x_top_left: Optional[int] = None,
                 y_top_left: Optional[int] = None,
                 x_bot_right: Optional[int] = None, y_bot_right: Optional[int] = None):
        self.parent_doc = parent_doc
        self.y_bot_right = y_bot_right
        self.x_bot_right = x_bot_right
        self.y_top_left = y_top_left
        self.x_top_left = x_top_left
        self.blocks = blocks
        self.word_list = [block.word for block in self.blocks]

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, item):
        return self.blocks[item]

    def get_blockset_by_query(self, query: Union[str, List[str]]) -> Block_t:
        """
        Check if the query word is present in the blockset or not
        """
        block_list = []
        for block in self.blocks:
            if fuzz.ratio(query, block.word) > 80:
                logger.debug('Perfect Match!')
                logger.debug('Query: %r', query)
                logger.debug(' Block Word: %r', block.word)
                logger.debug('Coordinates are [x_tl,y_tl,x_br, y_br]: %r %r %r %r', block.x_top_left, block.y_top_left,
                            block.x_bot_right,
                            block.y_bot_right)
                block_list.append(block)
                break
        return BlockSet(parent_doc=self.parent_doc, blocks=block_list)

    def get_synthetic_blockset(self) -> BlockSet_t:
        """
        Given a list of blocks create a synthetic blockset with appropriate x,y coordinates.
        Assuming that the x_top_left, y_top_left, x_bot_right, y_bot_right == None
        """
        x_top_left = min([block.x_top_left for block in self.blocks])
        y_top_left = min([block.y_top_left for block in self.blocks])
        x_bot_right = max([block.x_bot_right for block in self.blocks])
        y_bot_right = max([block.y_bot_right for block in self.blocks])
        return BlockSet(parent_doc=self.parent_doc, x_top_left=x_top_left, y_top_left=y_top_left, x_bot_right=x_bot_right,
                        y_bot_right=y_bot_right, blocks=self.blocks)

    def get_synthetic_block(self) -> Block_t:
        """
        Given a list of blocks return a synthetic block
        eg - Block("Invoice") + Block("Date") -> Block("Invoice Date")
        """
        x_top_left = min([block.x_top_left for block in self.blocks])
        y_top_left = min([block.y_top_left for block in self.blocks])
        x_bot_right = max([block.x_bot_right for block in self.blocks])
        y_bot_right = max([block.y_bot_right for block in self.blocks])
        word = [block.word for block in self.blocks]
        word = ' '.join(word)
        return Block(parent_doc=self.parent_doc, x_top_left=x_top_left, y_top_left=y_top_left, x_bot_right=x_bot_right,
                     y_bot_right=y_bot_right, word=word)


class Block(object):
    """
    Lowest level data structure. It is defined by the coordinates [x_top_left, y_top_left, x_bot_right, y_bot_right]
    and the word that is detected.
    """

    def __init__(self, parent_doc: HTMLParsingUtils, x_top_left: int, y_top_left: int, x_bot_right: int,
                 y_bot_right: int, word: str):
        self.parent_doc = parent_doc
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.x_bot_right = x_bot_right
        self.y_bot_right = y_bot_right
        self.word = word.strip()
        self.x_centre = int(self.x_top_left + (self.x_bot_right - self.x_top_left) / 2)
        self.y_centre = int(self.y_top_left + (self.y_bot_right - self.y_top_left) / 2)
        self.centre = [self.x_centre, self.y_centre]


class Page(object):

    def __init__(self, file_path: Optional[str]):
        self.page = HTMLParsingUtils(from_file=file_path)
        self.page_blockset = self.get_blockset()

    def get_parsed_values(self) -> object:
        """
        Objects are parsed sequentially in xpath. The function uses xpath matching to give
        title[A list of bbox] and word. Parsing is only done for class = 'ocrx_word'
        """
        # The bbox is sequentially listed
        title_list = Utils.split_bbox(self.page.match_xpath('.//span[@class="ocrx_word"]/@title'))
        text_list = self.page.match_xpath('.//span[@class="ocrx_word"]/text()')
        page = self.page.match_xpath('.//div[@class="ocr_page"]/@title')
        # Get bbox coordinates
        bbox_page = Utils.split_bbox_page(page)
        return title_list, text_list, bbox_page

    def get_blockset(self) -> BlockSet_t:
        """
        Returns all blocks in the page as a BlockSet data structure present in the page file of class='ocrx_word'
        """
        bbox_list, word_list, bbox_page = self.get_parsed_values()
        x_top_left_coord = [t[0] for t in bbox_list]
        y_top_left_coord = [t[1] for t in bbox_list]
        x_bot_right_coord = [t[2] for t in bbox_list]
        y_bot_right_coord = [t[3] for t in bbox_list]
        blockset = []
        for i in range(0, len(word_list)):
            blockset.append(Block(self.page, x_top_left_coord[i], y_top_left_coord[i], x_bot_right_coord[i],
                                  y_bot_right_coord[i],
                                  word_list[i]))
        return BlockSet(parent_doc=self.page, x_top_left=bbox_page[0], y_top_left=bbox_page[1],
                        x_bot_right=bbox_page[2], y_bot_right=bbox_page[3], blocks=blockset)
