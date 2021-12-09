import os
import sys
import pandas as pd

from utils.mappings import getDNColumns
from utils.fileUtils import *
from utils.columnNameToIndex import column_to_number

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy" )

#if no supplier  is null
if supplier == 'null':
    supplier = "Juicy"

if season == 'null':
    season = "FW21"

path = os.getcwd() + "/../Datanova-import/Suppliers/" + season + "/" + supplier + "/from-supplier/"

DNcolumnsIndexToName, DNcolumns = getDNColumns(path)

print("DNcolumns")
print(DNcolumns)
print(" ")
print(" ")


csvFiles, excelFiles = get_files(path)
print("Found CSVs: ", csvFiles)
print("Found excels: ", excelFiles)
print(DNcolumnsIndexToName)
newColumns = list(DNcolumnsIndexToName.keys())
print(newColumns)


frames = []
for fileNo,csvFile in enumerate(csvFiles):
    print("File no: ", fileNo, csvFile)
    csvDF = pd.read_csv(path + csvFile, usecols=DNcolumns, header=0, names=newColumns, delimiter=";")
    frames.append(csvDF)

allFilesDF = pd.concat(frames)
print(" ")
print(" ")
print(csvDF.head())
exit(0)
#allFilesDF.dropna(subset=['Antall'], inplace=True)

# for excelFile in excelFiles:
#     print("Reading ",excelFile)
#     excelDF = pd.read_excel(os.getcwd() + "/src/from-supplier/" + excelFile)

allFilesDF.drop([0], inplace=True)

print(" ")
print('Read csv:')
print(allFilesDF.info())
print(allFilesDF.head())

print(" ")
print(allFilesDF.iloc[0])
print(" ")
print(" ")
print(allFilesDF.iloc[1])
print(" ")
print(" ")
print(allFilesDF.iloc[2])

writeToFile(path, csvDF)