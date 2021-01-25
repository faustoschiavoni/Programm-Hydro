import pandas as pd
import re
import numpy.polynomial.polynomial as poly

Data_file = "Inputs/Data.dat"
Data_import = open(Data_file).readlines()
for i in range(len(Data_import)):
    if "param: Discount_Rate" in Data_import[i]:
        Discount_Rate = float(re.findall('\d+\.\d+', Data_import[i])[0])
    if "param: Ammortization" in Data_import[i]:
        Ammortization = int((re.findall('\d+', Data_import[i])[0]))
    if "param: Lifetime" in Data_import[i]:
        Lifetime = int((re.findall('\d+', Data_import[i])[0]))
    if "param: DMV" in Data_import[i]:
        DMV = float((re.findall('\d+\.\d+', Data_import[i])[0]))
    if "param: Giorni" in Data_import[i]:
        giorni = int((re.findall('\d+', Data_import[i])[0]))
    if "param: Portata_Nom" in Data_import[i]:
        Pnom = float(re.findall('\d+\.\d+', Data_import[i + 1])[0])#Pnom della Turbina A

xls = pd.ExcelFile('Inputs/Excel.xls')
df1 = pd.read_excel(xls, 'Duration_Curve')
df2 = pd.read_excel(xls, 'Hgross')
df3 = pd.read_excel(xls, 'Efficiency_1')

def Initialize_Duration_Curve(model, g):
    serie_portate = []
    for f in range(giorni):
        serie_portate += [df1.loc[f][1]-DMV] #così ho direttamente la Q_available
    return serie_portate[g-1]


def Initialize_Hgross(model, g):
    serie_Hgross = []
    for f in range(giorni):
        serie_Hgross += [df2.loc[f][1]]
    return serie_Hgross[g-1]

grado_poly = 4#2,3
def Initialize_Efficiency(model, g):
    serie_Efficiency = []
    serie_Portate = []
    for f in range(len(df3)):
        serie_Efficiency += [df3.loc[f][1]]
        serie_Portate += [df3.loc[f][0]]
    coefs = poly.polyfit(serie_Portate, serie_Efficiency, grado_poly)
    return coefs[g-1]


def Initialize_Qp_max_min():
    return df3.loc[0][0]*Pnom, df3.loc[len(df3)-1][0]*Pnom


def Initialize_Act():
    a = sum(1 / ((1 + Discount_Rate) ** f) for f in range(1, Ammortization + 1))
    b = sum(1 / ((1 + Discount_Rate) ** f) for f in range(Ammortization + 1, Lifetime + 1))
    return a, b
