import sys
import os
from pathlib import Path
import pandas as pd
from pandas.core.series import Series

def readJsonFile (path, fileName):
    p = Path(path + fileName)

    with p.open('r+') as file:
        fileString = file.read()
        fileString = '[' + fileString + ']'

    return pd.read_json(fileString)

def filePath(season, supplier):
    return os.getcwd() + "/../Datanova-import/Suppliers/" + \
    season + "/" + supplier + "/from-supplier/"

def get_files(path):
    csvFiles = [file for file in os.listdir(path) if file.endswith(".csv")]
    excelFiles = [file for file in os.listdir(
        path) if file.endswith(".xlsx") or file.endswith(".xls")]
    return csvFiles, excelFiles


def writeToFile(path, df):
    os.mkdir(path + "../to-retailer") if not os.path.exists(path +
                                                            "../to-retailer") else None
    file = path + "../to-retailer/datanova.csv"
    os.remove(file) if os.path.exists(file) else None
    df.to_csv(file, encoding='utf-8', index=False)

def findDuplicateColumnPresets(columns):
    columnHeadings = columns.index.tolist()
    columnAlphaNames = columns.values.tolist()

    print("Find dups in:")
    print(columnHeadings)
    print(columnAlphaNames)

    dups = dict()
    for i, val in enumerate(columnAlphaNames):
        if (val == columnAlphaNames[i-1]):
            dups[columnHeadings[i-1]] = columnHeadings[i]

    print("Found dups:", dups)
    return dups

def removeDuplicates(columns, duplicateColumnNames):
    for columnName, alphaValue in columns.copy().items():
        if (columnName in duplicateColumnNames):
            columns.drop(duplicateColumnNames[columnName], inplace=True)
    return columns

def readfiles(path, columns):
    print("\n")
    csvFiles, excelFiles = get_files(path)
    print("Found CSVs: ", csvFiles)
    print("Found excels: ", excelFiles)
    print("\n")

    sortedColumns = columns.sort_values()
    duplicateColumnNames = findDuplicateColumnPresets(sortedColumns)
    columns = removeDuplicates(columns, duplicateColumnNames)

    print(columns)

    frames = []
    for fileNo, csvFile in enumerate(csvFiles):
        try:
            csvDF = pd.read_csv(path + csvFile, usecols=columns.values,
                                header=0, names=columns.index, delimiter=",")
            frames.append(csvDF)
        except Exception as e:
            print("\nFile not ',' delimited: ", csvFile, " Try ';' delimter:")
            print("\tException:", e)
            try:
                csvDF = pd.read_csv(path + csvFile, usecols=columns.values,
                                    header=0, names=columns.index, delimiter=";")
                frames.append(csvDF)
            except Exception as e:
                print("\nFile not ';' delimited, either: ", csvFile)
                print("\tException:", e)
                continue
            else:
                print("Successfully read file", csvFile, "with ';' delimiter\n")
            finally:
                continue
        else:
            print("Successfully read file: ", csvFile, " with ',' delimiter\n")
    
    if not frames:
        print("No files found")
        sys.exit(1)

    df = pd.concat(frames)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    if (len(duplicateColumnNames) > 0):
        for columnName in duplicateColumnNames:
            pos = df.columns.get_loc(columnName)
            df.insert(pos+1, duplicateColumnNames[columnName], df[columnName])

    print("Read data:")
    print(df.head())

    return df

def getDNColumnsAndPresets ():
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-datanova.json")

    columnPresetsStandard = readJsonFile(
        os.getcwd() + "/src/import-templates/", "standard-setup-datanova.json")

    columnPresetsSuppliers = readJsonFile(
        os.getcwd() + "/src/import-templates/", "suppliers-setup-datanova.json")

    return allDNColumns, columnPresetsStandard, columnPresetsSuppliers


def getColumnsAndPresets (target):
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-" + target + ".json")

    columnPresetsStandard = readJsonFile(
        os.getcwd() + "/src/import-templates/", "standard-setup-" + target + ".json")

    columnPresetsSuppliers = readJsonFile(
        os.getcwd() + "/src/import-templates/", "suppliers-setup-shopify.json")

    return allDNColumns, columnPresetsStandard, columnPresetsSuppliers