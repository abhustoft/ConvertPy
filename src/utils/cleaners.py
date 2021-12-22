from utils.fileUtils import readJsonFile
import os


def setDNColumnTypes(df):
    df['Antall'].fillna(0, inplace=True)
    df['Antall'] = df['Antall'].astype('int16')
    df['Handle'] = df['Handle'].astype('string')
    df['Fargenavn'] = df['Fargenavn'].astype('string')
    df['Varenavn'] = df['Varenavn'].astype('string')
    df['Str-navn'] = df['Str-navn'].astype('string')
    df['eanplu'] = df['eanplu'].astype('string')
    df['Innkjøpspris'] = df['Innkjøpspris'].astype('float')
    df['Salgspris'] = df['Salgspris'].astype('float')

    return df


def addDNColumns(df, supplier):
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-datanova.json")

    columnPresetsStandard = readJsonFile(
        os.getcwd() + "/src/import-templates/", "standard-setup-datanova.json")

    columnPresetsSuppliers = readJsonFile(
        os.getcwd() + "/src/import-templates/", "suppliers-setup-datanova.json")

    # print(columnPresetsStandard.info())
    # print(columnPresetsSuppliers.info())

    rows = len(df.index)

    for column in allDNColumns.columns.tolist():
        if column in columnPresetsStandard.columns:
            onlist = columnPresetsStandard[column][0]
            df[column] = onlist * rows
        elif column not in df.columns:
            df[column] = [" "] * rows

        if supplier in columnPresetsSuppliers.columns:
            firstRow            = columnPresetsSuppliers[supplier].tolist()[0]["firstDataRow"]        if "firstDataRow"        in columnPresetsSuppliers[supplier].tolist()[0] else 1
            thousandDivider     = columnPresetsSuppliers[supplier].tolist()[0]["thousandDivider"]     if "thousandDivider"     in columnPresetsSuppliers[supplier].tolist()[0] else ''
            decimalDivider      = columnPresetsSuppliers[supplier].tolist()[0]["decimalDivider"]      if "decimalDivider"      in columnPresetsSuppliers[supplier].tolist()[0] else ''
            purchasePriceFactor = columnPresetsSuppliers[supplier].tolist()[0]["purchasePriceFactor"] if "purchasePriceFactor" in columnPresetsSuppliers[supplier].tolist()[0] else 1
            coldict             = columnPresetsSuppliers[supplier].tolist()[0]["columns"]
            
            print("\n",supplier)
            print(column)
            print("firstRow", firstRow)
            print("thousandDivider", thousandDivider)
            print("decimalDivider", decimalDivider)
            print("purchasePriceFactor", purchasePriceFactor)
            print(coldict)


    df = df.loc[:, allDNColumns.columns.tolist()]

    return df
