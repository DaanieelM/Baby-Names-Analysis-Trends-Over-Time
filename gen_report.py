import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#Opening the first 10 lines
with open('data/babynames/yob1882.txt', 'r') as file:
    for i in range(10):
        print(file.readline().strip())

names1882 = pd.read_csv('data/babynames/yob1882.txt', names=['name', 'sex', 'births'])

names1882

names1882.groupby('sex').births.sum()

years = range(1880, 2023)  # Range of years
pieces = []  # List to store data
columns = ['name', 'sex', 'births', 'year']

for year in years:
    path = f'data/babynames/yob{year}.txt'
    if os.path.exists(path):  # Check if the file exists
        frame = pd.read_csv(path, names=columns)
        frame['year'] = year  # Add a year column
        pieces.append(frame)  # Add the data to the list
    else:
        print(f'File does not exist for year: {year}')

# Concatenate all pieces into one table
names = pd.concat(pieces, ignore_index=True)

print(names.head())  # Preview the first rows

names['year']

total_births = names.pivot_table('births', index='year', columns='sex', aggfunc='sum')

total_births.plot(title='Total number of births by gender and age')

#100 Most Common Names
def get_top100(group):
    return group.sort_values(by='births', ascending=False)[:100]
grouped = names.groupby(['year', 'sex'])
top100 = grouped.apply(get_top100)
top100.reset_index(inplace=True, drop=True)
 
# Get last letter
names['last_letter'] = names['name'].str[-1]


table = names.pivot_table(
    values='births',
    index='last_letter',
    columns=['sex', 'year'],
    aggfunc='sum'
)


subtable = table.loc[:, (slice(None), [1990, 2000, 2010])]
print(subtable.head())

# Data normalization
subtable_sum = subtable.sum()
letter_prop = subtable.div(subtable_sum, axis=1)

# Data visualization: popularity of last letters for Men and Women
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

colors = ['royalblue', 'seagreen', 'gold']

# for Man
letter_prop['M'].plot(
    kind='bar',
    rot=0,
    ax=axes[0],
    title='Male',
    color=colors,
    legend=True
)

# for Woman
letter_prop['F'].plot(
    kind='bar',
    rot=0,
    ax=axes[1],
    title='Female',
    color=colors,
    legend=True
)

plt.tight_layout()
plt.show()

letter_prop_full = table.div(table.sum(), axis=1)
dny_ts = letter_prop_full.loc[['d', 'n', 'y'], 'M'].transpose()

print(dny_ts.head())

# Visualize changes over time
dny_ts.plot(
    figsize=(10, 6),
    title="Proportion of Names Ending in 'd', 'n', and 'y' (Male)",
    linewidth=2
)
plt.xlabel('Year')
plt.ylabel('Proportion')
plt.legend(title="Last Letter")
plt.grid()
plt.show()
