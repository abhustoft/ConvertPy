import os

def get_files(path):
    csvFiles = [file for file in os.listdir(path) if file.endswith(".csv")]
    excelFiles = [file for file in os.listdir(path) if file.endswith(".xlsx") or file.endswith(".xls")]
    return csvFiles, excelFiles

def writeToFile (path, df):
    os.mkdir(path + "../to-retailer") if not os.path.exists(path + "../to-retailer") else None
    file = path + "../to-retailer/datanova.csv"
    os.remove(file) if os.path.exists(file) else None
    df.to_csv(file, encoding='utf-8', index=False)