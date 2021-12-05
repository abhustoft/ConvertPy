import os

def get_files():
    csvFiles = [file for file in os.listdir("src/from-supplier/") if file.endswith(".csv")]
    excelFiles = [file for file in os.listdir("src/from-supplier/") if file.endswith(".xlsx") or file.endswith(".xls")]
    return csvFiles, excelFiles