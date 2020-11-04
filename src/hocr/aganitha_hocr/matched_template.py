from typing import Union, Any
from src.hocr.aganitha_hocr.object_model import BlockSet, Region
from src.hocr.aganitha_hocr.template import Template


class MatchedTemplate(object):
    def __init__(self, parent_template: Template, computer_params: str, matched_blocks: BlockSet,
                 matched_regions: Region):
        self.parent_template = parent_template
        self.computer_params = computer_params  # table width, column width, update column width after detection
        self.matched_blocks = matched_blocks
        self.matched_regions = matched_regions

    def extract(self, matched_params: Union[BlockSet, Region]) -> Any:
        pass
