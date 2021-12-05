import pandas as pd
import os

# junior = pd.read_csv(os.getcwd() + "/pandas/" + "Junior.csv")

# print(junior)


junior = pd.read_excel(os.getcwd() + "/Importfiles/" + "Junior2.xlsx", dtype={'EAN/UPC': str})

print('Original:')
print(junior.head())
condition = (junior['Nett'] > 273)
print('Condition:')
print(condition.head())

biggies = junior[condition]

print('Removed rows with low Nett values:')
print(biggies.head())

#print(junior.info())
#print(junior.shape)
# print(junior.columns)
# print(junior.loc[2])



#junior.columns = [col.lower() for col in junior]
print('Info:')
print(junior.info())
#print(junior.isnull().sum())

clean = junior.dropna()
#print(clean.info())
#print(clean.isnull().sum())

ean = junior['EAN/UPC']
print('EAN row:')
print(ean)

junior.rename(columns={
        'EAN/UPC': 'EAN',
        'Name 1': 'Target'
    }, inplace=True)
#print(junior['EAN'])

ean.fillna('delete', inplace=True)
print('EAN replaced:')
print(ean)


subset = junior[['EAN', 'Target']]

print(subset.head())

row = subset.loc[2]

print('Row:')
print(row)



def rating_function(x):
    if x >= 300.0:
        return "good"
    else:
        return "bad"

junior["rating_category"] = junior["Nett"].apply(rating_function)

print('After apply:')
print(junior[["Nett", "rating_category"]].head())
print(junior.head())
