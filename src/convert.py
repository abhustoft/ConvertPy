import os
import sys
import pandas as pd

from utils.mappings import getDNColumns
from utils.fileUtils import *
from utils.columnNameToIndex import column_to_number

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy")

# if no supplier  is null
if supplier == 'null':
    supplier = "Juicy"

if season == 'null':
    season = "FW21"

path = os.getcwd() + "/../Datanova-import/Suppliers/" + \
    season + "/" + supplier + "/from-supplier/"

DNcolumnsNames, DNcolumnsIndices = getDNColumns(path)

csvFiles, excelFiles = get_files(path)
print("Found CSVs: ", csvFiles)
print("Found excels: ", excelFiles)

frames = []
for fileNo, csvFile in enumerate(csvFiles):
    csvDF = pd.read_csv(path + csvFile, usecols=DNcolumnsIndices,
                        header=0, names=DNcolumnsNames, delimiter=";")
    frames.append(csvDF)

allFilesDF = pd.concat(frames)
allFilesDF.reset_index(inplace=True)
allFilesDF.drop(columns=['index'], inplace=True)

# for excelFile in excelFiles:
#     print("Reading ",excelFile)
#     excelDF = pd.read_excel(os.getcwd() + "/src/from-supplier/" + excelFile)


print(" ")
print('Read csv:')
print(allFilesDF.head())

writeToFile(path, csvDF)
