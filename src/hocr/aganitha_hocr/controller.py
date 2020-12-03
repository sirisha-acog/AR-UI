from src.hocr.aganitha_hocr.object_model import Page
from src.hocr.aganitha_hocr.template_repo.MMS import MMS
from src.hocr.aganitha_hocr.template_repo.GroupM import GroupM
from src.hocr.aganitha_hocr.template_repo.OMG_USA_Media import OMG
from src.hocr.aganitha_hocr.template_repo.Squared import Squared
from src.hocr.aganitha_hocr.template_repo.IPG import IPG
from src.hocr.aganitha_hocr.template_repo.Katz_Media_Group import Katz
import logging
import json
import os
import csv
import pandas as pd

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # page = Page('/Users/adarsh/work/ar-automation/tmp/09.24.20-lb83198-1-17-addl-doc-01.jpg.hocr.hocrjs.html')
    # template = Katz()
    # extracted_values = template.execute(page.page_blockset)
    # print(extracted_values)
    # Path to Data - '/Users/adarsh/work/ar-automation/new_data'
    os.listdir('/Users/adarsh/work/ar-automation/new_data')
    # val = input("Enter your template: ")
    val = 'MMS'
    if val == 'MMS':
        template = MMS()
        path_of_files = '/Users/adarsh/work/ar-automation/new_data/MMS'
        filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
        i = 0
        for file in filenames:
            print(file)
            page = Page(path_of_files + '/' + file)
            extracted_values = template.execute(page.page_blockset)
            # Dump Into JSON
            with open('/Users/adarsh/work/ar-automation/output/json/MMS/' + file + 'output.json', 'w') as json_file:
                logger.debug("Dumping into JSON")
                json.dump(extracted_values, json_file, indent=4)

            # Dump Into CSV
            keys = []
            for key, value in extracted_values.items():
                keys.append(key)
            df = pd.DataFrame(index=range(100), columns=keys)
            for i in range(len(extracted_values['Invoice Number'])):
                df['DATE'][i] = extracted_values["DATE"]
                df['CHECK NUMBER'][i] = extracted_values['CHECK NUMBER']
                df['AMOUNT PAID'][i] = extracted_values['AMOUNT PAID']
                df['Invoice Date'][i] = extracted_values['Invoice Date'][i]
                df['Invoice Number'][i] = extracted_values['Invoice Number'][i]
                df['Amount'][i] = extracted_values['Amount'][i]
            df = df.dropna()
            df.to_csv('/Users/adarsh/work/ar-automation/output/csv/MMS/' + file + 'output.csv',index=False)
            print(extracted_values)
