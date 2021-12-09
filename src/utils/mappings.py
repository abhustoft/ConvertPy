import pandas as pd
import os
from pathlib import Path
from utils.columnNameToIndex import column_to_number
import string

def getDNColumns(path):
    p = Path(path + "column-map-datanova.json")

    with p.open('r+') as file:
        fileString = file.read()          # reads the file in as a long string
        fileString = '[' + fileString + ']'  # adds brackets to the start and end of the string

    rawMapDF     = pd.read_json(fileString)

    # Column letters to index number
    for name, values in rawMapDF.iteritems():
        rawMapDF[name] = column_to_number(values[0])

    names        = rawMapDF.columns.to_series()
    flippedMapDF = rawMapDF.append(names,ignore_index=True)
    columnNumber   = rawMapDF.iloc[0]
    flippedMapDF.columns = columnNumber
    flippedMapDF.drop(index=0, inplace=True)

    print("mod_df2: ")
    print(flippedMapDF.head())
    print(" ")

    columnsDict = flippedMapDF.to_dict('records')[0]
    columnsIndexToName = dict((value, key) for key, value in columnsDict.items())
    return columnsIndexToName, flippedMapDF.columns
