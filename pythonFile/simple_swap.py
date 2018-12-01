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


def calculate_score(paths, cities_df_dict):
    sum_distance = 0
    prev_x, prev_y = cities_df_dict['X'][0], cities_df_dict['Y'][0]
    prev_is_prime = False
    for i, city in enumerate(paths):
        x, y = cities_df_dict['X'][city], cities_df_dict['Y'][city]
        is_prime = cities_df_dict['IsPrime'][city]
        sum_distance += distance(prev_x, prev_y, x, y,prev_is_prime, i % 10 == 0)
        prev_x, prev_y = x, y
        prev_is_prime = is_prime
    return sum_distance


def calculate_short_score(paths, cities_df_dict):
    sum_distance = 0
    prev_x, prev_y = cities_df_dict['X'][0], cities_df_dict['Y'][0]
    prev_is_prime = False
    for i, city in enumerate(paths):
        x, y = cities_df_dict['X'][city], cities_df_dict['Y'][city]
        is_prime = cities_df_dict['IsPrime'][city]
        sum_distance += distance(prev_x, prev_y, x, y,
                                 prev_is_prime, i == 3)
        prev_x, prev_y = x, y
        prev_is_prime = is_prime
    return sum_distance

def swap(x, y):
    swap = x
    x = y
    y = swap
    return x, y


def main():
    DEBUG = False
    DEBUG_SIZE = 10000

    cities_df = pd.read_csv('../input/cities.csv')
    cities_df['IsPrime'] = cities_df['CityId'].apply(isprime)
    cities_df_dict = cities_df.to_dict()
    submission_df = pd.read_csv('submission.csv')
    if DEBUG:
    #   cities_df = cities_df[:DEBUG_SIZE]
        submission_df = submission_df[:DEBUG_SIZE]

    pre_full_score = calculate_score(submission_df['Path'], cities_df_dict)
    print('Before:' + str(pre_full_score))

    pbar = tqdm(total=len(submission_df))
    step = 9
    while step + 2 < len(submission_df) - 1:
        change = True
        short_df = submission_df['Path'][step-2:step+3].tolist()
        pre_score = calculate_short_score(short_df, cities_df_dict)
        short_df[2], short_df[1] = swap(short_df[2], short_df[1])
        score = calculate_short_score(short_df, cities_df_dict)
        if score > pre_score:
            short_df[2], short_df[1] = swap(short_df[2], short_df[1])
            change = False
        pre_score = score

        short_df[2], short_df[3] = swap(short_df[2], short_df[3])
        score = calculate_short_score(short_df, cities_df_dict)
        if score > pre_score:
            short_df[2], short_df[3] = swap(short_df[2], short_df[3])
            change = change or False
        if change:
            submission_df['Path'][step-2:step+3] = short_df
        step += 10
        pbar.update(10)
    pbar.close()
    score = calculate_score(submission_df['Path'], cities_df_dict)
    print('After :' + str(score))

    # save submission.csv
    saved = False
    if pre_full_score == score:
        saved = True
    number = 0
    while saved == False:
        Filename = '{:.3f}submit{:02}.csv'.format(score, number)
        if os.path.exists(Filename) == False:
            submission_df.to_csv(Filename, index=False)
            saved = True
        else:
            number += 1

    # Plot tour and save png file
    # lines = [[(cities.X[submission_df['Path'][i]], cities.Y[submission_df['Path'][i]]),
    #           (cities.X[submission_df['Path'][i+1]], cities.Y[submission_df['Path'][i+1]])] for i in range(0, len(cities)-1)]
    # lc = mc.LineCollection(lines, linewidths=2)
    # fig, ax = pl.subplots(figsize=(20, 20))
    # ax.set_aspect('equal')
    # ax.add_collection(lc)
    # ax.autoscale()
    # Figname = str(int(score)) + 'submit' + str(number).zfill(2) + '.png'
    # fig.savefig(Figname)


if __name__ == "__main__":
    main()
