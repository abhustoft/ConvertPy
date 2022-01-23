import sys
from utils.mappings import getColumnsMapping
from utils.cleaners import *
from utils.fileUtils import *
from utils.columnNameToIndex import alpha_to_index

season, supplier = sys.argv[1:] if len(sys.argv) == 3 else ('2021FW', "Juicy")
path = filePath(season, supplier)

# Datanova ****************************************
columnsDN  = getColumnsMapping(path, "column-map-datanova.json")
fileDataDN = readfiles(path, columnsDN)
fileDataDN['Antall'].fillna(0, inplace=True)
fileDataDN = setColumnTypes(fileDataDN)

allColumnsDN, columnPresetsStandardDN, columnPresetsSuppliersDN = getDNColumnsAndPresets()
allColumnsDN = fillWithEmptyRows(allColumnsDN, len(fileDataDN.index))
allColumnsDN = setStandardPresets(allColumnsDN, columnPresetsStandardDN)
allColumnsDN = setSupplierPresets(allColumnsDN, columnPresetsSuppliersDN, supplier)
allColumnsDN = fillFileData(allColumnsDN, fileDataDN, season)
    
testing = allColumnsDN.loc[[0,1,2], ['Lev-varenr-','eanplu', 'Leverandørnr-', 'Fargenavn', 'Antall']]
print(testing.head)

allColumnsDN.drop(columns=['index'], inplace=True)

writeToFile(path, allColumnsDN)

# Shopify ****************************************
columnsShopify = getColumnsMapping(path, "column-map-shopify.json") #All used columns are un Shopify map
fileDataShopify = readfiles(path, columnsShopify) # readfiles should handle Shopify columns
fileDataShopify = setColumnTypes(fileDataShopify)
allColumnsSH, columnPresetsStandardSH, columnPresetsSuppliersSH = getColumnsAndPresets("shopify")



print(fileDataShopify.head())

# print(allColumnsSH.head())
# print(columnPresetsStandardSH.head())
# print(columnPresetsSuppliersSH.head())

