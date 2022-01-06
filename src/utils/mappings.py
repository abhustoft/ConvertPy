from utils.columnNameToIndex import alpha_to_index
from utils.fileUtils import readJsonFile


def reorder_columns(dataframe, col_name, position):
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe


def getDNColumnsMapping(path):
    columnsMapAlphaNumeric = readJsonFile(path, "column-map-datanova.json")
    columnsMapIndices = columnsMapAlphaNumeric.apply(alpha_to_index)
    return columnsMapIndices.sort_values()
