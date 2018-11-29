import sympy
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from subprocess import getoutput

check = getoutput("../shellFile/linkernPrepare.sh")
print(check)

cities = pd.read_csv('../input/cities.csv', index_col=['CityId'])
