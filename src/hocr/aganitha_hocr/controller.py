from src.hocr.aganitha_hocr.object_model import Block, BlockSet, Page
from src.hocr.aganitha_hocr.template_repo.MMS import MMS
if __name__ == "__main__":
    page = Page('/home/adarsh/work/ar-automation/tmp/07.07.20-lb83143-1-2-addl-doc-01.jpg.hocr')
    mms = MMS()
    status = mms.match(page.page_blockset)
    if status:
        extracted_values = mms.extract(page.page_blockset)
    else:
        print("Template did not match")
