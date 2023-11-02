#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
print("Reading the CSV file...")
df = pd.read_csv("atom_data.csv")

# Sort the data
print("Sorting the data...")
df = df.sort_values(by="eng")

# Group the data into bins
diff = df['eng'].diff()
groups = (diff >= 1).cumsum()

# Create histograms for relative eng values within each group
for group_id, group_data in df.groupby(groups):
    print(f"Creating histogram for Group {group_id}...")
    min_eng = group_data['eng'].min()
    max_eng = group_data['eng'].max()
    num_eng = len(group_data)
    relative_eng = (group_data['eng'] - min_eng) * 2625.5 # Convert Ha to kJ/mol
    plt.hist(relative_eng, bins=100)  # You can adjust the number of bins as needed
    plt.title(f'{num_eng} datapoints from {round(min_eng)} to {round(max_eng)}')
    plt.xlabel('Relative energy (kJ/mol)')
    plt.ylabel('Frequency')
    plt.savefig(f'{num_eng}_{round(min_eng)}_{round(max_eng)}.png')
    plt.close()

print("All relative energy histograms saved.")
