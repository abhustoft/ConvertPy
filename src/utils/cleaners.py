from utils.fileUtils import readJsonFile
from utils.fileUtils import getDNColumnsAndPresets
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

def fillWithEmptyRows(df, noOfRows):
    df.loc[0] = " " # Blank out 'A', 'B', 'C' etc. column positions
    emptyRow = df.loc[[0]]

    for i in range(noOfRows-1):
        df = pd.concat([df,emptyRow]) 

    df.reset_index(inplace=True)
    return df

def setStandardPresets(allDNColumns, columnPresetsStandard):
    for column in columnPresetsStandard:
        allDNColumns[column] = columnPresetsStandard[column].values[0]
    return allDNColumns

def setSupplierPresets(allDNColumns, columnPresetsSuppliers, supplier):
    presetsDict = columnPresetsSuppliers[supplier].array[0]
    columns = presetsDict['columns']
    columnsDict = dict(columns)
    # del presetsDict['columns']
    # presets = {**presetsDict, **columnsDict}
    # What to do with firstDataRow and friends?

    for column in columnsDict:
        allDNColumns[column] = columnsDict[column]

    return allDNColumns

def addDNColumns(fileData):
    allDNColumns, columnPresetsStandard, columnPresetsSuppliers = getDNColumnsAndPresets()
    allDNColumns = fillWithEmptyRows(allDNColumns, len(fileData.index))

    # Fill columns with data from file
    for column in fileData.columns:
        values = fileData[column].values
        column = 'Lev-varenr-' if column == 'Handle' else column
        allDNColumns[column] = values
        
    allDNColumns = setStandardPresets(allDNColumns, columnPresetsStandard)
    allDNColumns = setSupplierPresets(allDNColumns, columnPresetsSuppliers, "HustAndClaire")

    ff = allDNColumns.loc[[0,1,2], ['MVA%','eanplu', 'Leverandørnr-', 'Fargenavn', 'Antall']]
    print(ff.head)

    allDNColumns.drop(columns=['index'], inplace=True)
    return allDNColumns
