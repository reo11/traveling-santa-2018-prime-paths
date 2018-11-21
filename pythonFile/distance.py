#%%
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib
import math
import os
from sympy import isprime
from calculate_distance import calculate_score

DEBUG = True
DEBUG_SIZE = 100000
print(os.listdir("../input"))

cities_df = pd.read_csv('../input/cities.csv')
sample_submission = pd.read_csv('simple_nearest.csv')

if DEBUG:
    cities_df = cities_df[:DEBUG_SIZE]
    sample_submission = sample_submission[:DEBUG_SIZE]
#%%
cities_df = cities_df.sample(frac=1)
#%%
cities_df.head(15)
#%%
cities_df.describe()

#%%
cities_df = cities_df.sort_values(by=['X','Y'])

cities_val  = cities_df.values
xy = cities_df.values[:,1]+cities_df.values[:,2]
cities_valT = np.concatenate([cities_val, xy.reshape(-1, 1)], axis=1)
cities_df = pd.DataFrame(cities_valT, columns=['num', 'X', 'Y','XY'])
cities_df = cities_df.sort_values(by=['XY'])
cities_df = cities_df.drop(columns='XY')
cities_df.head()
#%%
value = sample_submission.values
mapped_list = map(lambda x: x[0], value)
value = list(mapped_list)

#%%
# value = range(10)
# print(value)
figure = plt.figure(figsize=(8,8))
plt.scatter(cities_df['X'], cities_df['Y'], c=value, cmap='Blues')
plt.colorbar()
#%%
sample_submission.head(10)
#%%
len(cities_df)
#%%
cities_df.info()

# Score Calculation
#%%
score = calculate_score(sample_submission['Path'])
print(score)

sample_submission.to_csv('to_submit.csv', index=None)
