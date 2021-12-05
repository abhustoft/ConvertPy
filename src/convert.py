import os
import sys
import pandas as pd

from utils.mappings import getDNColumns
from utils.fileUtils import *
from utils.columnNameToIndex import column_to_number

season, supplier = sys.argv[1:]
path = os.getcwd() + "/../Datanova-import/Suppliers/" + season + "/" + supplier + "/from-supplier/"

DNcolumnsIndexToName = getDNColumns(path)
csvFiles, excelFiles = get_files(path)
print("Found CSVs: ", csvFiles)
print("Found excels: ", excelFiles)

for fileNo,csvFile in enumerate(csvFiles):
    print("File no: ", fileNo, csvFile)
    csvDF = pd.read_csv(path + csvFile, delimiter=";")

    for index in DNcolumnsIndexToName:
        csvDF.rename(columns={csvDF.columns[index]: DNcolumnsIndexToName[index]}, inplace=True)

    deleteColumns = set(csvDF.columns) - set(DNcolumnsIndexToName.values())
    csvDF.drop(deleteColumns, axis=1, inplace=True)

# for excelFile in excelFiles:
#     print("Reading ",excelFile)
#     excelDF = pd.read_excel(os.getcwd() + "/src/from-supplier/" + excelFile)

print('Read csv:')
print(csvDF.info())
print(csvDF.head())

writeToFile(path, csvDF)
