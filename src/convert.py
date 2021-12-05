import pandas as pd
import os
import sys
from utils.mappings import getDNColumns
from utils.fileUtils import *
from utils.columnNameToIndex import column_to_number

season = sys.argv[1]
supplier = sys.argv[2]

print("Fetching data from: ", season, " ", supplier)
path = os.getcwd() + "/../Datanova-import/Suppliers/" + season + "/" + supplier + "/from-supplier/"
print("Fetching data from path: ", path)


DNcolumnsIndexToName = getDNColumns(path)
csvFiles, excelFiles = get_files(path)
print("Found CSVs: ", csvFiles)
print("Found excels: ", excelFiles)

for csvFile in csvFiles:
    csvDF = pd.read_csv(path + csvFile, delimiter=";")

    for index in DNcolumnsIndexToName:
        csvDF.rename(columns={csvDF.columns[index]: DNcolumnsIndexToName[index]}, inplace=True)

    # Drop columns not in DNcolumnsIndexToName
    allColumnNames = set(csvDF.columns)
    DNColumnNames = set(DNcolumnsIndexToName.values())
    deleteColumns = allColumnNames - DNColumnNames
    csvDF.drop(deleteColumns, axis=1, inplace=True)

# for excelFile in excelFiles:
#     print("Reading ",excelFile)
#     excelDF = pd.read_excel(os.getcwd() + "/src/from-supplier/" + excelFile)

print('Read csv:')
print(csvDF.info())
print(csvDF.head())

writeToFile(path, csvDF)
