from src.hocr.aganitha_hocr.object_model import BlockSet, Block

# TODO: Given a query containing multiple strings we should be able to identify blocksets with some tolerance T.


def top(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    return context


def bot(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    pass


def left(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    pass


def right(context: BlockSet, argument: float = 100, percentage: bool = True) -> BlockSet:
    return context


def nearest(context: BlockSet, anchor: Block, axis: str) -> BlockSet:
    return context
