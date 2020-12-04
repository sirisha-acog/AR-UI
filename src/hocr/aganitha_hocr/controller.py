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
import time
import pandas as pd

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # page = Page('/Users/adarsh/work/ar-automation/tmp/09.24.20-lb83198-1-17-addl-doc-01.jpg.hocr.hocrjs.html')
    # template = Katz()
    # extracted_values = template.execute(page.page_blockset)
    # print(extracted_values)
    # Path to Data - '/Users/adarsh/work/ar-automation/new_data'
    t0 = time.time()
    os.listdir('/Users/adarsh/work/ar-automation/new_data')
    # val = input("Enter your template: ")
    template = MMS()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/MMS'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]

    for file in filenames:
        page = Page(path_of_files + '/' + file)
        extracted_values = template.execute(page.page_blockset)
        # Dump Into JSON
        with open('/Users/adarsh/work/ar-automation/experiment/json/MMS/' + file + 'output.json', 'w') as json_file:
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
        df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/MMS/' + file + 'output.csv', index=False)

    template = GroupM()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/GroupM'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
    for file in filenames:
        page = Page(path_of_files + '/' + file)
        extracted_values = template.execute(page.page_blockset)

        # Dump Into JSON
        with open('/Users/adarsh/work/ar-automation/experiment/json/GroupM/' + file + 'output.json', 'w') as json_file:
            logger.debug("Dumping into JSON")
            json.dump(extracted_values, json_file, indent=4)

        # Dump Into CSV
        keys = []
        for key, value in extracted_values.items():
            keys.append(key)
        df = pd.DataFrame(index=range(100), columns=keys)
        for i in range(len(extracted_values["Invoice number"])):
            df["Check number"][i] = extracted_values["Check number"][0]
            df["Check date"][i] = extracted_values["Check date"][0]
            df["Check amount"][i] = extracted_values["Check amount"][0]
            df["Total amount"][i] = extracted_values["Total amount"][0]
            df["Invoice number"][i] = extracted_values["Invoice number"][i]
            df["Period"][i] = extracted_values["Period"][i]
            df["Net Amount"][i] = extracted_values["Net Amount"][i]
        df = df.dropna()
        df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/GroupM/' + file + 'output.csv', index=False)

    template = OMG()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/OMG'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
    for file in filenames:
        page = Page(path_of_files + '/' + file)
        extracted_values = template.execute(page.page_blockset)

        # Dump into JSON
        with open('/Users/adarsh/work/ar-automation/experiment/json/OMG/' + file + 'output.json', 'w') as json_file:
            logger.debug("Dumping into JSON")
            json.dump(extracted_values, json_file, indent=4)

        # Dump Into CSV
        keys = []
        for key, value in extracted_values.items():
            keys.append(key)
        df = pd.DataFrame(index=range(100), columns=keys)
        try:
            for i in range(len(extracted_values["Invoice Number"])):
                df["Date"][i] = extracted_values["Date"][0]
                df["Check Number"][i] = extracted_values["Check Number"][0]
                df["Check Amount"][i] = extracted_values["Check Amount"][0]
                df["Invoice Number"][i] = extracted_values["Invoice Number"][i]
                df["Invoice Date"][i] = extracted_values["Invoice Date"][i]
                df["Gross Amount"][i] = extracted_values["Gross Amount"][i]
                df["Net Amount"][i] = extracted_values["Net Amount"][i]
            df = df.dropna()
            df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/OMG/' + file + 'output.csv', index=False)
        except IndexError:
            print("INDEXERROR:Removing file ", file)

    template = Squared()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/22Squared'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
    i = 0
    for file in filenames:
        page = Page(path_of_files + '/' + file)
        extracted_values = template.execute(page.page_blockset)

        with open('/Users/adarsh/work/ar-automation/experiment/json/22Squared/' + file + 'output.json', 'w') as json_file:
            logger.debug("Dumping into JSON")
            json.dump(extracted_values, json_file, indent=4)

        # Dump Into CSV
        keys = []
        for key, value in extracted_values.items():
            keys.append(key)
        df = pd.DataFrame(index=range(100), columns=keys)
        try:
            for i in range(len(extracted_values["Invoice Number"])):
                df["Date"][i] = extracted_values["Date"][0]
                df["Check Number"][i] = extracted_values["Check Number"][0]
                df["Invoice Number"][i] = extracted_values["Invoice Number"][i]
                df["Invoice Date"][i] = extracted_values["Invoice Date"][i]
                df["Gross Amount"][i] = extracted_values["Gross Amount"][i]
                df["Discount"][i] = extracted_values["Discount"][i]
                df["Net"][i] = extracted_values["Net"][i]
                df["Net Less Discount"][i] = extracted_values["Net Less Discount"][i]
                df["Gross Total"][i] = extracted_values["Gross Total"][0]
                df["Discount Total"][i] = extracted_values["Discount Total"][0]
                df["Net Total"][i] = extracted_values["Net Total"][0]
                df["Net Less Discount Total"][i] = extracted_values["Net Less Discount Total"][0]

            df = df.dropna()
            df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/22Squared/' + file + 'out    put.csv', index=False)
        except IndexError:
            print("INDEXERROR:Removing file ", file)

    template = Katz()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/Katz'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
    katz = 0
    for file in filenames:
        try:
            page = Page(path_of_files + '/' + file)
            extracted_values = template.execute(page.page_blockset)
            # Write to Json
            with open('/Users/adarsh/work/ar-automation/experiment/json/Katz/' + file + 'output.json',
                      'w') as json_file:
                logger.debug("Dumping into JSON")
                json.dump(extracted_values, json_file, indent=4)
            # Write to csv
            keys = []
            for key, value in extracted_values.items():
                keys.append(key)
            df = pd.DataFrame(index=range(100), columns=keys)
            try:
                for i in range(len(extracted_values["Stn-Invoice"])):
                    df["Stn-Invoice"][i] = extracted_values["Stn-Invoice"][i]
                    df["Voucher"][i] = extracted_values["Voucher"][i]
                    df["Grs-Order"][i] = extracted_values["Grs-Order"][i]
                    df["Grs-Billed"][i] = extracted_values["Grs-Billed"][i]
                    df["Paid Amount"][i] = extracted_values["Paid Amount"][i]
                df = df.dropna()
                df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/Katz/' + file + 'output.csv',
                      index=False)

            except IndexError:
                print("INDEXERROR:Removing file ", file)

        except ValueError:
            katz = katz + 1
            print("Katz Value Error")

    template = IPG()
    path_of_files = '/Users/adarsh/work/ar-automation/new_data/IPG'
    filenames = [_ for _ in os.listdir(path_of_files) if _.endswith(r'.html')]
    i = 0
    for file in filenames:
        page = Page(path_of_files + '/' + file)
        extracted_values = template.execute(page.page_blockset)
        with open('/Users/adarsh/work/ar-automation/experiment/json/IPG/' + file + 'output.json',
                  'w') as json_file:
            logger.debug("Dumping into JSON")
            json.dump(extracted_values, json_file, indent=4)

        # Dump Into CSV
        keys = []
        for key, value in extracted_values.items():
            keys.append(key)
        df = pd.DataFrame(index=range(100), columns=keys)
        try:
            for i in range(len(extracted_values["Invoice Number"])):
                df["Date"][i] = extracted_values["Date"][0]
                df["Check Number"][i] = extracted_values["Check Number"][0]
                df["Invoice Number"][i] = extracted_values["Invoice Number"][i]
                df["Invoice Date"][i] = extracted_values["Invoice Date"][i]
                df["Invoice Period"][i] = extracted_values["Invoice Period"][i]
                df["Net Amount"][i] = extracted_values["Net Amount"][i]
                df["Check Total"][i] = extracted_values["Check Total"][0]

            df = df.dropna()
            if len(df) > 0:
                df.to_csv('/Users/adarsh/work/ar-automation/experiment/csv/IPG/' + file + 'output.csv', index=False)
                logger.debug("Ignored %r", file)
        except IndexError:
            print("Index Error")
    t1 = time.time()
    logger.debug("TOTAL EXECUTION TIME: %r", float(t1-t0))
    # print(katz)
