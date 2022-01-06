from utils.fileUtils import readJsonFile
import pandas as pd
import os
import numpy as np


def setDNColumnTypes(df):
    df['Antall'].fillna(0, inplace=True)
    df['Antall'] = df['Antall'].astype('string')
    df['Handle'] = df['Handle'].astype('string')
    df['Fargenavn'] = df['Fargenavn'].astype('string')
    df['Varenavn'] = df['Varenavn'].astype('string')
    df['Str-navn'] = df['Str-navn'].astype('string')
    df['eanplu'] = df['eanplu'].astype('string')
    df['Innkjøpspris'] = df['Innkjøpspris'].astype('string')
    df['Salgspris'] = df['Salgspris'].astype('string')

    return df


def addDNColumns(fileData, supplier):
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-datanova.json")

    columnPresetsStandard = readJsonFile(
        os.getcwd() + "/src/import-templates/", "standard-setup-datanova.json")

    columnPresetsSuppliers = readJsonFile(
        os.getcwd() + "/src/import-templates/", "suppliers-setup-datanova.json")

    noOfRows = len(fileData.index)

    print(allDNColumns.loc[[0], ['eanplu', 'Merkenavn', 'Aldersgruppe']])
    
    allDNColumns.loc[0] = " "
    emptyRow = allDNColumns.loc[[0]]
    print(allDNColumns.loc[[0], ['eanplu', 'Merkenavn', 'Aldersgruppe']])

    for i in range(noOfRows-1):
        allDNColumns = pd.concat([allDNColumns,emptyRow]) 

    allDNColumns.reset_index(inplace=True)

    print(allDNColumns.loc[[0,1,2], ['eanplu', 'Merkenavn', 'Aldersgruppe']])
    print(fileData.columns)
    print(allDNColumns.columns)

    for column in fileData.columns:
        fileVals = fileData[column].values
        if column == 'Handle':
            column = 'Lev-varenr-'

        print(type(fileVals), fileVals[0], fileVals[1])

        if column in allDNColumns.columns:
            to = allDNColumns.loc[:,column]
            allDNColumns.loc[:, column] = fileVals
        
        print(allDNColumns.loc[[0,1,2], ['eanplu', 'Merkenavn', 'Aldersgruppe']])

    
    ff = allDNColumns.loc[[0,1,2], ['eanplu', 'Salgspris', 'Fargenavn', 'Antall']]

    allDNColumns.drop(columns=['index'], inplace=True)
    print(ff.head)

    return allDNColumns
