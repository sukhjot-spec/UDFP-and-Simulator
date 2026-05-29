import pandas as pd
from simulation import simulate_batch

def generate_dataset(n_batches=20, DT=.1, total_time = 30):
    dfs = []
    for i in range(n_batches):
        print(f"running batch {i}")
        batch_df = simulate_batch(batchID=i, DT=DT, time=total_time)
        dfs.append(batch_df)
    return pd.concat(dfs, ignore_index=True)