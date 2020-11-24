from src.hocr.aganitha_hocr.object_model import Page
from src.hocr.aganitha_hocr.template_repo.MMS import MMS
from src.hocr.aganitha_hocr.template_repo.GroupM import GroupM
from src.hocr.aganitha_hocr.template_repo.OMG_USA_Media import OMG
from src.hocr.aganitha_hocr.template_repo.Squared import Squared
import logging
import json
import os
import csv
import pandas as pd
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    page = Page('/home/adarsh/work/ar-automation/tmp/07.22.20-lb83197-1-3-addl-doc-01.jpg.hocr.hocrjs.html')
    template = Squared()
    extracted_values = template.execute(page.page_blockset)
    print(extracted_values)
    #extracted_values.to_csv('/home/adarsh/work/ar-automation/output/csv/22squared_1.csv', index=False)