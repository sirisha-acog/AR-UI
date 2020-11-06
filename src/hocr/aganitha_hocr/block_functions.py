from src.hocr.aganitha_hocr.object_model import Region
from src.hocr.aganitha_hocr.object_model import BlockSet
from src.hocr.aganitha_hocr.object_model import Block
from src.hocr.aganitha_hocr.object_model import HOCRDoc
from scipy.spatial import distance
import logging
logger = logging.getLogger(__name__)


def nearest(blockset: BlockSet, anchor_block: Block, axis: str):
    """
    Find the nearest block in the specified axis to context: eg DateBlock
    """
    for block in blockset:
        dist = (distance.euclidean(block.centre, anchor_block.centre))

