from src.hocr.aganitha_hocr.object_model import Page
from src.hocr.aganitha_hocr.template_repo.MMS import MMS
from src.hocr.aganitha_hocr.template_repo.GroupM import GroupM
import logging
import json
import os
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    page = Page('/home/adarsh/work/ar-automation/tmp/07.09.20-lb83197-1-5-addl-doc-01.jpg.hocr.hocrjs.html')
    template = GroupM()
    extracted_values = template.execute(page.page_blockset)
    print(extracted_values)
    # path = '/home/adarsh/work/ar-automation/data/MMS-remmitance-hocr'
    # for file in os.listdir(path):
    #     if file.endswith(".html"):
    #         print("For File --------> ", os.path.join(path, file))
    #         page = Page('/home/adarsh/work/ar-automation/data/MMS-remmitance-hocr/07.07.20-lb83293-1-4-addl-doc-01.jpg.hocr.hocrjs.html')
    #         page = Page('/Users/abhishek/Documents/CoxMedia-Crestfin/GroupM-SRA-1.hocr')
    #         template = MMS()
    #         extracted_values = template.execute(page.page_blockset)
    #         t = [block.word for block in page.page_blockset.blocks]
    #         if "TOTALS" in t:
    #             print("present")
    #         with open('/home/adarsh/work/ar-automation/data/output_json/mms3.json', 'w') as json_file:
    #              json.dump(extracted_values, json_file, indent=4)
