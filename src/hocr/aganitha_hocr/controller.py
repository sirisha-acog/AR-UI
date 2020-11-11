from src.hocr.aganitha_hocr.object_model import Page
from src.hocr.aganitha_hocr.template_repo.GroupM import GroupM
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    page = Page('/home/adarsh/work/ar-automation/tmp/07.07.20-lb83143-1-2-addl-doc-01.jpg.hocr')
    # page = Page('/Users/abhishek/Documents/CoxMedia-Crestfin/GroupM-SRA-1.hocr')
    template = GroupM()
    logger.debug("Match Output: %r", template.match(page.page_blockset))
    logger.info("Extracted Params: %r", template.extract(page.page_blockset))
