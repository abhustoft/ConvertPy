import sys
import os
from pathlib import Path
import pandas as pd

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


def readfiles(path, DNcolumns):
    csvFiles, excelFiles = get_files(path)
    print("Found CSVs: ", csvFiles)
    print("Found excels: ", excelFiles)
    print(DNcolumns.index)
    print(DNcolumns.values)
    #DNColumnsIndices = DNcolumns)

    frames = []
    for fileNo, csvFile in enumerate(csvFiles):
        try:
            csvDF = pd.read_csv(path + csvFile, usecols=DNcolumns.values,
                                header=0, names=DNcolumns.index, delimiter=",")
            frames.append(csvDF)
        except Exception as e:
            print("File not ',' delimited: ", csvFile, " Try ';' delimter:")
            print("\t", e)
            try:
                csvDF = pd.read_csv(path + csvFile, usecols=DNcolumns.values,
                                    header=0, names=DNcolumns.index, delimiter=";")
                frames.append(csvDF)
            except Exception as e:
                print("File not ';' delimited, either: ", csvFile)
                print("\t", e)
                continue
            else:
                print("Successfully read file", csvFile, "with ';' delimiter")
            finally:
                continue
        else:
            print("Successfully read file: ", csvFile, " with ',' delimiter")
    
    if not frames:
        print("No files found")
        sys.exit(1)

    df = pd.concat(frames)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    return df
