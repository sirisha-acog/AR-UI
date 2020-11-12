from src.hocr.aganitha_hocr.object_model import Page
from src.hocr.aganitha_hocr.template_repo.MMS import MMS
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    page = Page('/home/adarsh/work/ar-automation/tmp/07.07.20-lb83143-1-2-addl-doc-01.jpg.hocr')
    # page = Page('/Users/abhishek/Documents/CoxMedia-Crestfin/GroupM-SRA-1.hocr')
    template = MMS()
    print(template.execute(page.page_blockset))

