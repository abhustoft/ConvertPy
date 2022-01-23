from utils.columnNameToIndex import alpha_to_index
from utils.fileUtils import readJsonFile

def reorder_columns(dataframe, col_name, position):
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe

def getColumnsMapping(path, file):
    columnsMapAlphaNumeric = readJsonFile(path, file)
    columnsMapIndices = columnsMapAlphaNumeric.apply(alpha_to_index)
    return columnsMapIndices.sort_values()
