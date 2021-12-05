import pandas as pd
import os
from pathlib import Path
from utils.columnNameToIndex import column_to_number
import string

def getDNColumns():
    p = Path(os.getcwd() + "/src/from-supplier/" + "column-map-datanova.json")

    with p.open('r+') as file:
        fileString = file.read()          # reads the file in as a long string
        fileString = '[' + fileString + ']'  # adds brackets to the start and end of the string

    columnsDF = pd.read_json(fileString)

    # Column letters to index number
    for name, values in columnsDF.iteritems():
        columnsDF[name] = column_to_number(values[0])

    columnsDict = columnsDF.to_dict('records')[0]
    columnsIndexToName = dict((value, key) for key, value in columnsDict.items())
    return columnsIndexToName
