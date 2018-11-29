from concorde.tsp import TSPSolver
from matplotlib import collections as mc
import numpy as np
import pandas as pd
import time
import pylab as pl
import math
import os
from sympy import isprime
from tqdm import tqdm

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
    count = 0
    for i, city in enumerate(paths):
        x, y = cities_df_dict['X'][city], cities_df_dict['Y'][city]
        is_prime = cities_df_dict['IsPrime'][city]
        sum_distance += distance(prev_x, prev_y, x, y,prev_is_prime, i % 10 == 0)
        prev_x, prev_y = x, y
        if i % 10 == 0:
            if prev_is_prime == False:
                count += 1
        prev_is_prime = is_prime
    print('Not Prime : ' + str(count))
    print('Prime     : ' + str(int(len(paths)/10)-count))
    return sum_distance


def main():
    cities = pd.read_csv('../input/cities.csv')

    # Instantiate solver
    solver = TSPSolver.from_data(
        cities.X,
        cities.Y,
        norm="EUC_2D"
    )

    tour_data = solver.solve(time_bound=60.0, verbose=True, random_seed=42)
    submission_df = pd.DataFrame({'Path': np.append(tour_data.tour, [0])})
    score = calculate_score(submission_df['Path'])
    print(score)
    saved = False
    number = 0
    while saved == False:
        Filename = str(int(score)) + 'submit' + str(number).zfill(2) + '.csv'
        if os.path.exists(Filename) == False:
            submission_df.to_csv(Filename, index=False)
            saved = True
        else:
            number += 1

    # make better using prime
    # cities_df = cities
    # cities_df['IsPrime'] = cities_df['CityId'].apply(isprime)
    # cities_df_dict = cities_df.to_dict()

    # best_submission = submission_df
    # prev_is_prime = True
    # for i, city in enumerate(tqdm(submission_df['Path'])):
    #     is_prime = cities_df_dict['IsPrime'][city]
    #     if (i % 10 == 0)and(prev_is_prime == False):
    #         for j in range(9):
    #             if i-1-j < 0 or i-1+j > len(submission_df['Path'])-1:
    #                 break
    #             preNum = int(best_submission['Path'][i-1-j])
    #             nextNum = int(best_submission['Path'][i-1+j])
    #             if cities_df_dict['IsPrime'][preNum] == True:
    #                 best_score = calculate_score(best_submission['Path'][i-10:i+10])
    #                 temp = best_submission['Path'][i-1]
    #                 best_submission['Path'][i-1] = best_submission['Path'][i-1-j]
    #                 best_submission['Path'][i-1-j] = temp
    #                 new_score = calculate_score(best_submission['Path'][i-10:i+10])
    #                 if best_score > new_score:
    #                     temp = best_submission['Path'][i-1]
    #                     best_submission['Path'][i - 1] = best_submission['Path'][i-1-j]
    #                     best_submission['Path'][i-1-j] = temp
    #                     continue
    #                 else:
    #                     break
    #             elif cities_df_dict['IsPrime'][nextNum] == True:
    #                 best_score = calculate_score(best_submission['Path'][i-10:i+10])
    #                 temp = best_submission['Path'][i-1]
    #                 best_submission['Path'][i-1] = best_submission['Path'][i-1+j]
    #                 best_submission['Path'][i-1+j] = temp
    #                 new_score = calculate_score(best_submission['Path'][i-10:i+10])
    #                 if best_score > new_score:
    #                     temp = best_submission['Path'][i-1]
    #                     best_submission['Path'][i - 1] = best_submission['Path'][i-1-j]
    #                     best_submission['Path'][i-1-j] = temp
    #                     continue
    #                 else:
    #                     break
    #     prev_is_prime = is_prime
    # score = calculate_score(best_submission['Path'])
    # print(score)
    # saved = False
    # number = 0
    # while saved == False:
    #     Filename = str(int(score)) + 'submit' + str(number).zfill(2) + '.csv'
    #     if os.path.exists(Filename) == False:
    #         best_submission.to_csv(Filename, index=False)
    #         saved = True
    #     else:
    #         number += 1

    # Plot tour
    lines = [[(cities.X[tour_data.tour[i]],cities.Y[tour_data.tour[i]]),(cities.X[tour_data.tour[i+1]],cities.Y[tour_data.tour[i+1]])] for i in range(0,len(cities)-1)]
    lc = mc.LineCollection(lines, linewidths=2)
    fig, ax = pl.subplots(figsize=(20,20))
    ax.set_aspect('equal')
    ax.add_collection(lc)
    ax.autoscale()
    Figname = str(int(score)) + 'submit' + str(number).zfill(2) + '.png'
    fig.savefig(Figname)

if __name__ == "__main__":
    main()
