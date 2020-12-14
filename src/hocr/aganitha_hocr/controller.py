from aganitha_hocr.object_model import Page
from aganitha_hocr.template_repo.MMS import MMS
from aganitha_hocr.template_repo.GroupM import GroupM
from aganitha_hocr.template_repo.OMG_USA_Media import OMG
from aganitha_hocr.template_repo.Squared import Squared
from aganitha_hocr.template_repo.IPG import IPG
from aganitha_hocr.template_repo.Katz_Media_Group import Katz
from aganitha_hocr.template_repo.Other import OtherDoc
import logging
import json
import os
import csv
import time
import pandas as pd
import pathlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def main(filepath):
    # filepath = '/Users/adarsh/test_vaccine.jpg.json.hocr.hocrjs.html'
    page = Page(filepath)
    templates = [MMS(), GroupM(), OMG(), Squared(), IPG(), Katz()]
    extracted_values = None
    file = os.path.basename(filepath)
    for template in templates:
        try:
            extracted_values = template.execute(page.page_blockset)
            # print(extracted_values)
            return file, extracted_values, template
        except Exception:
            logger.debug("Moving to new template")


def batch_processing(path):
    pass


def extract_MMS(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/MMS/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/MMS/').mkdir(parents=True, exist_ok=True)
    # Dump Into JSON
    with open(path_to_store + '/json/MMS/' + filename + 'output.json', 'w') as json_file:
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
    df.to_csv(path_to_store + '/csv/MMS/' + filename + 'output.csv', index=False)


def extract_GroupM(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/GroupM/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/GroupM/').mkdir(parents=True, exist_ok=True)

    # Dump Into JSON
    with open(path_to_store + '/json/GroupM/' + filename + 'output.json', 'w') as json_file:
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
    df.to_csv(path_to_store + '/csv/GroupM/' + filename + 'output.csv', index=False)


def extract_OMG(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/OMG/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/OMG/').mkdir(parents=True, exist_ok=True)

    # Dump into JSON
    with open(path_to_store + '/json/OMG/' + filename + 'output.json', 'w') as json_file:
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
        df.to_csv(path_to_store + '/csv/OMG/' + filename + 'output.csv', index=False)
    except IndexError:
        print("INDEXERROR:Removing file ", filename)


def extract_Squared(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/22Squared/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/22Squared/').mkdir(parents=True, exist_ok=True)

    # Dump into JSON
    with open(path_to_store + '/json/22Squared/' + filename + 'output.json', 'w') as json_file:
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
        df.to_csv(path_to_store + '/csv/22Squared/' + filename + 'output.csv', index=False)
    except IndexError:
        print("INDEXERROR:Removing file ", filename)


def extract_Katz(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/Katz/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/Katz/').mkdir(parents=True, exist_ok=True)

    # Dump to JSON
    with open(path_to_store + '/json/Katz/' + filename + 'output.json', 'w') as json_file:
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
        df.to_csv(path_to_store + '/csv/Katz/' + filename + 'output.csv',
                  index=False)

    except IndexError:
        print("INDEXERROR:Removing file ", filename)


def extract_IPG(filename, extracted_values, path_to_store):
    # Create Paths if they don't exist
    pathlib.Path(path_to_store + '/json/IPG/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_to_store + '/csv/IPG/').mkdir(parents=True, exist_ok=True)

    # Dump into JSON
    with open(path_to_store + '/json/IPG/' + filename + 'output.json', 'w') as json_file:
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
            df.to_csv(path_to_store + '/csv/IPG/' + filename + 'output.csv', index=False)
    except IndexError:
        print("Index Error")


def extract_data(filename, template, extracted_params, store_path):
    if extracted_params is None:
        print("No templates matched.")
        print("Added " + " to excluded templates")
    if isinstance(template, MMS):
        logger.debug("Inside MMS")
        extract_MMS(filename=filename, extracted_values=extracted_params, path_to_store=store_path)

    elif isinstance(template, GroupM):
        logger.debug("Inside GroupM")
        extract_GroupM(filename=filename, extracted_values=extracted_params, path_to_store=store_path)

    elif isinstance(template, OMG):
        logger.debug("Inside OMG")
        extract_OMG(filename=filename, extracted_values=extracted_params, path_to_store=store_path)

    elif isinstance(template, IPG):
        logger.debug("Inside IPG")
        extract_IPG(filename=filename, extracted_values=extracted_params, path_to_store=store_path)

    elif isinstance(template, Squared):
        logger.debug("Inside 22Squared")
        extract_Squared(filename=filename, extracted_values=extracted_params, path_to_store=store_path)

    elif isinstance(template, Katz):
        logger.debug("Inside Katz")
        extract_Katz(filename=filename, extracted_values=extracted_params, path_to_store=store_path)


if __name__ == "__main__":
    file, extracted_params, temp = main(
        filepath='/Users/adarsh/work/ar-automation/new_data/MMS/07.07.20-lb83143-1-2-addl-doc-01.jpg.hocr.hocrjs.html')

    store_path = '/Users/adarsh/work/ar-automation/test2'
    extract_data(file,temp, extracted_params, store_path)
