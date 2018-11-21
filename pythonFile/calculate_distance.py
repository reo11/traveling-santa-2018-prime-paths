import math
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sympy import isprime
# Score Calculation
# The function to get the distance between the cities.
def distance(x1, y1, x2, y2, prev_is_prime, is_10th):
    # Every 10th step is 10% more lengthy unless coming from a prime CityId.
    cost_factor = 1.1 if is_10th and not prev_is_prime else 1.0
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * cost_factor

# The function to calculate score.
# The beginning and end of the paths must be City'0'.
def calculate_score(paths):
    cities_df = pd.read_csv('../input/cities.csv')
    cities_df['IsPrime'] = cities_df['CityId'].apply(isprime)
    cities_df_dict = cities_df.to_dict()

    sum_distance = 0
    prev_x, prev_y = cities_df_dict['X'][0], cities_df_dict['Y'][0]
    prev_is_prime = False

    for i, city in enumerate(paths):
        x, y = cities_df_dict['X'][city], cities_df_dict['Y'][city]
        is_prime = cities_df_dict['IsPrime'][city]

        sum_distance += distance(prev_x, prev_y, x, y, prev_is_prime, i % 10 == 0)
        prev_x, prev_y = x, y
        prev_is_prime = is_prime

    return sum_distance
