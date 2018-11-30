import numpy as np
import pandas as pd
import time
from tqdm import tqdm
from calculate_distance import calculate_score

if __name__ == '__main__':
    cities_df = pd.read_csv('../input/cities.csv')

    cities_val  = cities_df.values
    xy = cities_df.values[:,1]+cities_df.values[:,2]
    cities_valT = np.concatenate([cities_val, xy.reshape(-1, 1)], axis=1)
    cities_df = pd.DataFrame(cities_valT, columns=['num', 'X', 'Y','XY'])
    cities_df = cities_df.sort_values(by=['XY'])
    cities_df = cities_df.drop('XY', axis=1)

    ixy  = cities_df.values # CityId(or index), X, Y
    R    = []        # Result list of CityId
    start = time.time()
    for i in tqdm(range(len(ixy))):
        d    = (ixy[:, 1] - ixy[0, 1]) ** 2 + (ixy[:, 2] - ixy[0, 2]) ** 2 # the distance from last choiced city
        ixyd = np.concatenate([ixy, d.reshape(-1, 1)], axis=1)
        argi = np.argsort(ixyd[:, 3]) # Argsorted index by the distance
        ixyd = ixyd[argi]
        R.append(int(ixyd[0, 0]))
        ixy = ixyd[1:, :-1] # update cities data

    s = pd.read_csv('../input/sample_submission.csv')
    s['Path'] = np.array(R + [0]) # Return 0

    s.to_csv('simple_nearest2.csv', index=False)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    sample_submission = pd.read_csv('simple_nearest2.csv')
    score = calculate_score(sample_submission['Path'])
    print(score)