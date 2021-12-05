import pandas as pd
import os
from utils.mappings import getDNColumns
from utils.fileUtils import get_files
from utils.columnNameToIndex import column_to_number

DNcolumnsIndexToName = getDNColumns()
csvFiles, excelFiles = get_files()
#print(csvFiles)
#print(excelFiles)

#junior = pd.read_excel(os.getcwd() + "/src/from-supplier/" + "junior.xlsx", dtype={'EAN/UPC': str}, usecols=columns)
#junior = pd.read_excel(os.getcwd() + "/src/from-supplier/" + "junior.xlsx", usecols=columns)

print("  ")
print("Looper csv fil:")

for csvFile in csvFiles:
    csvDF = pd.read_csv(os.getcwd() + "/src/from-supplier/" + csvFile, delimiter=";")

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
csvDF.to_csv(os.getcwd() + "/src/to_retailer/datanova.csv", encoding='utf-8', index=False)
# print(excelDF.info())