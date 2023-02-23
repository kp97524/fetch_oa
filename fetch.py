import sys
import pandas as pd
import numpy as np

def fetch_fn(points, file):
    df = pd.read_csv(file)
    #sorting dataframe by timestamp in ascending order(oldest time comes first)
    df = df.sort_values(by='timestamp')

    # find total points for every user
    payers, pts = df['payer'].to_numpy(), df['points'].to_numpy()
    tot_points = np.zeros(len(np.unique(payers)), dtype=int)
    np.add.at(tot_points, np.searchsorted(np.unique(payers), payers), pts)

    # iterate through every row of dataframe and spend points
    for _, row in df.iterrows():
        payer_idx = np.searchsorted(np.unique(payers), row.payer)
        if row.points > 0 and row.points <= points and points > 0:
            points = points - row.points
            tot_points[payer_idx] -= row.points
        elif row.points < 0 and points > 0:
            tot_points[payer_idx] += abs(row.points)
            points += abs(row.points)
        elif row.points > 0 and row.points > points and points > 0:
            tot_points[payer_idx] -= points
            points -= points
            break

    result = {p: t for p, t in zip(np.unique(payers), tot_points)}
    return result

points = sys.argv[1]
file = sys.argv[2]
final_points = fetch_fn(int(points), file)
print(final_points)
