import sys
from utils.cleaners import addDNColumns, setDNColumnTypes
from utils.mappings import getDNColumnsMapping
from utils.fileUtils import *
from utils.columnNameToIndex import alpha_to_index

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy")
path = filePath(season, supplier)
DNcolumns = getDNColumnsMapping(path)

fileData = readfiles(path, DNcolumns)
fileData = setDNColumnTypes(fileData)
fullData = addDNColumns(fileData)
writeToFile(path, fullData)
