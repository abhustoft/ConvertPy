from utils.columnNameToIndex import column_to_number
from utils.fileUtils import readJsonFile


def reorder_columns(dataframe, col_name, position):
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe


def getDNColumnsMapping(path):
    columnsMapping = readJsonFile(path, "column-map-datanova.json")

    # Column letters to index number
    for name, values in columnsMapping.iteritems():
        columnsMapping[name] = column_to_number(values[0])

    # Sort the columns
    columnIndices = columnsMapping.iloc[0].to_list()
    sortedIndices = sorted(columnIndices)

    mappingTuples = []
    tupleIndex = 0
    # Loop over data columnsMapping
    for name, values in columnsMapping.iteritems():
        mappingTuples.append((name, values[0]))

    def takeSecond(elem):
        return elem[1]

    mappingTuples.sort(key=takeSecond)

    sortedColumnNames = []
    sortedColumnIndices = []
    for aTuple in mappingTuples:
        sortedColumnNames.append(aTuple[0])
        sortedColumnIndices.append(aTuple[1])

    return sortedColumnNames, sortedColumnIndices
