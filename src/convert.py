import os
import sys
import pandas as pd
from numpy import empty
from utils.cleaners import addDNColumns, setDNColumnTypes

from utils.mappings import getDNColumnsMapping
from utils.fileUtils import *
from utils.columnNameToIndex import column_to_number

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy")
path = filePath(season, supplier)
DNcolumnsNames, DNcolumnsIndices = getDNColumnsMapping(path)

df = readfiles(path, DNcolumnsNames, DNcolumnsIndices)
df = setDNColumnTypes(df)
df = addDNColumns(df)
writeToFile(path, df)
