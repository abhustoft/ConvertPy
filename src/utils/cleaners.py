from utils.fileUtils import readJsonFile
from utils.fileUtils import getDNColumnsAndPresets
import pandas as pd
import os
import re
import numpy as np
import hashlib


def setColumnTypes(df):
    for column in df:
        df[column] = df[column].astype('string')
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
    supplierPresetsDict = columnPresetsSuppliers[supplier].array[0]
    columns = supplierPresetsDict['columns']
    supplierColumnsDict = dict(columns)
    
    # del presetsDict['columns']
    # presets = {**presetsDict, **columnsDict}
    # What to do with firstDataRow and friends?

    for column in supplierColumnsDict:
        allDNColumns[column] = supplierColumnsDict[column]

    return allDNColumns

def fillFileData(allDNColumns, fileData, season):
    for columnName in fileData.columns:
        shortSeason = season.replace('20', '') + "&"

        if (columnName == 'Handle'):
            handles = fileData[columnName].values
            colors = fileData['Fargenavn'].values
            for i, val in enumerate(handles):
                size = fileData['Str-navn'].values[i].strip()
                color = fileData['Fargenavn'].values[i].strip()
                hash = hashlib.md5(color.encode('utf-8')).hexdigest()[:8]
                colors[i] = hash
                handles[i] = shortSeason + size + "@" + re.sub(r'\s+', '',  val) + "-" + hash

        renamedColumn = 'Lev-varenr-' if columnName == 'Handle' else columnName
        allDNColumns[renamedColumn] = fileData[columnName].values
    
    return allDNColumns
    



