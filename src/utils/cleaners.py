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


def addDNColumns(df):
    allDNColumns = readJsonFile(
        os.getcwd() + "/src/import-templates/", "importTemplate-datanova.json")

    rows = len(df.index)
    emptyList = [" "] * rows

    for column in allDNColumns.columns.tolist():
        if column not in df.columns:
            df[column] = emptyList

    df = df.loc[:, allDNColumns.columns.tolist()]
    return df
