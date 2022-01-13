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


def readfiles(path, columns):
    print("\n")
    csvFiles, excelFiles = get_files(path)
    print("Found CSVs: ", csvFiles)
    print("Found excels: ", excelFiles)
    cleanedColumns = Series(dict(columns)) #Remove dups ? Need to flip, then flip back
    print("\nOriginal column list:\n", columns)
    print("\nnames:\n", columns.index)
    print("\nvalues:\n", columns.values)
    print("\nCleaned column names:\n", cleanedColumns.index)
    print("\nCleaned column values:\n", cleanedColumns.values)

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

    return df

def getDNColumnsAndPresets ():
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-datanova.json")

    columnPresetsStandard = readJsonFile(
        os.getcwd() + "/src/import-templates/", "standard-setup-datanova.json")

    columnPresetsSuppliers = readJsonFile(
        os.getcwd() + "/src/import-templates/", "suppliers-setup-datanova.json")

    return allDNColumns, columnPresetsStandard, columnPresetsSuppliers