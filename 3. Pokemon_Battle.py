import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os

dfcom = pd.read_csv('combats.csv')
dfpok = pd.read_csv('pokemon.csv')
dftest = pd.read_csv('tests.csv')
dfpok.dropna(subset=['Name'], inplace=True)

print(len(np.sort(dfcom['First_pokemon'].unique())))


print(dfpok.columns)
dfpok1 = dfpok[['#', 'Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].copy()
print(len(np.sort(dfpok1['#'].unique())))

# print(dfpok1['Name'][dfpok1['Name'].isin(['Pikachu', 'Raichu'])])
dfpok1['sum'] = dfpok1.sum(axis=1)

print(dfpok1.head())

# # listpower1 = []
# # listpower2 = []
# # # for i in dfcom['First_pokemon'].values:
# # #     if i in dfpok1['#'].values:
# # #         listpower1.append(dfpok1['sum'][dfpok1['#'] == i].values[0])
# # #     else:
# # #         listpower1.append(np.nan)
# # #
# # # for i in dfcom['Second_pokemon'].values:
# # #     if i in dfpok1['#'].values:
# # #         listpower2.append(dfpok1['sum'][dfpok1['#'] == i].values[0])
# # #     else:
# # #         listpower2.append(np.nan)
# #
# #
# # dfcom['sum1'] = listpower1
# # dfcom['sum2'] = listpower2
#
# dfcom.dropna(inplace=True)
#
# print(dfcom.head())
#
# from sklearn.ensemble import RandomForestClassifier
# modelRFR = RandomForestClassifier(n_estimators=20)
# modelRFR.fit(dfcom.drop('Winner', axis=1), dfcom['Winner'])









import joblib

joblib.dump(dfpok1, 'dfpok1pokemon2')

