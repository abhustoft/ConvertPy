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
    try:
        csvDF = pd.read_csv(path + csvFile, usecols=DNcolumnsIndices,
                            header=0, names=DNcolumnsNames, delimiter=",")
        frames.append(csvDF)
    except Exception as e:
        print("Error in file, not ',' delimiter: ", csvFile)
        print("\t", e)
        try:
            csvDF = pd.read_csv(path + csvFile, usecols=DNcolumnsIndices,
                                header=0, names=DNcolumnsNames, delimiter=";")
            frames.append(csvDF)
        except Exception as e:
            print("Error in file, note '; delimiter, either: ", csvFile)
            print("\t",e)
            continue
        else:
            print("Successfully read file", csvFile, "with ';' delimiter")
        finally:
            continue
    else:
        print("Successfully read file: ", csvFile, " with ',' delimiter")

allFilesDF = pd.concat(frames)
allFilesDF.reset_index(inplace=True)
allFilesDF.drop(columns=['index'], inplace=True)
allFilesDF['Antall'].fillna(0, inplace=True)
allFilesDF['Antall'] = allFilesDF['Antall'].astype('int16')
allFilesDF['Handle'] = allFilesDF['Handle'].astype('string')
allFilesDF['Fargenavn'] = allFilesDF['Fargenavn'].astype('string')
allFilesDF['Varenavn'] = allFilesDF['Varenavn'].astype('string')
allFilesDF['Str-navn'] = allFilesDF['Str-navn'].astype('string')
allFilesDF['eanplu'] = allFilesDF['eanplu'].astype('string')
allFilesDF['Innkjøpspris'] = allFilesDF['Innkjøpspris'].astype('float')
allFilesDF['Salgspris'] = allFilesDF['Salgspris'].astype('float')

# for excelFile in excelFiles:
#     print("Reading ",excelFile)
#     excelDF = pd.read_excel(os.getcwd() + "/src/from-supplier/" + excelFile)


print(" ")
print('Read csv:')
print(allFilesDF.head())
print(allFilesDF.info())

writeToFile(path, csvDF)
