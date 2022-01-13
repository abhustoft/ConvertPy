import sys
from utils.cleaners import setDNColumnTypes
from utils.mappings import getDNColumnsMapping, getShopifyColumnsMapping
from utils.cleaners import fillWithEmptyRows
from utils.cleaners import setStandardPresets
from utils.cleaners import setSupplierPresets
from utils.cleaners import fillFileData
from utils.fileUtils import *
from utils.columnNameToIndex import alpha_to_index

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy")
path = filePath(season, supplier)
DNcolumns = getDNColumnsMapping(path)
Shopifycolumns = getShopifyColumnsMapping(path) #All used columns are un Shopify map

fileData = readfiles(path, DNcolumns)
#fileData = readfiles(path, Shopifycolumns)
fileData = setDNColumnTypes(fileData)

allDNColumns, columnPresetsStandard, columnPresetsSuppliers = getDNColumnsAndPresets()
allDNColumns = fillWithEmptyRows(allDNColumns, len(fileData.index))
allDNColumns = setStandardPresets(allDNColumns, columnPresetsStandard)
allDNColumns = setSupplierPresets(allDNColumns, columnPresetsSuppliers, supplier)
allDNColumns = fillFileData(allDNColumns, fileData, season)
    
testing = allDNColumns.loc[[0,1,2], ['Lev-varenr-','eanplu', 'Leverandørnr-', 'Fargenavn', 'Antall']]
print(testing.head)

allDNColumns.drop(columns=['index'], inplace=True)

writeToFile(path, allDNColumns)
