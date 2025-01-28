import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Open the first 10 lines of a file to preview its content
file_path = 'data/babynames/yob1992.txt'
with open(file_path, 'r') as file:
    for i in range(10):
        print(file.readline().strip())

# Read the 1992 dataset and display its content
names1992 = pd.read_csv(file_path, names=['name', 'sex', 'births'])
print("\nPreview of 1992 data:")
print(names1992.head())

# Calculate total births grouped by gender for 1992
total_births_1992 = names1992.groupby('sex').births.sum()
print("\nTotal births by gender in 1992:")
print(total_births_1992)

# Process data from all years and combine it into a single DataFrame
years = range(1990, 2020)  # Range of years
pieces = []  # List to store data
columns = ['name', 'sex', 'births']

print("\nProcessing data for all years...")
for year in years:
    path = f'data/babynames/yob{year}.txt'
    if os.path.exists(path):  # Check if the file exists
        frame = pd.read_csv(path, names=columns)
        frame['year'] = year  # Add a year column
        pieces.append(frame)  # Add the data to the list
    else:
        print(f'File does not exist for year: {year}')

# Combine all yearly data into one DataFrame
names = pd.concat(pieces, ignore_index=True)
print("\nCombined data preview:")
print(names.head())

# Create a pivot table showing total births by gender and year
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc='sum')

# Plot the total number of births over time
total_births.plot(title='Total Number of Births by Gender')
plt.xlabel('Year')
plt.ylabel('Number of Births')
plt.grid()
plt.show()

# Identify the 100 most common names for each year and gender
def get_top100(group):
    return group.sort_values(by='births', ascending=False)[:100]

grouped = names.groupby(['year', 'sex'])
top100 = grouped.apply(get_top100).reset_index(drop=True)

print("\nTop 100 names for a sample year (e.g., 1992):")
print(top100[top100['year'] == 1992].head())

# Analyze the popularity of last letters in names
names['last_letter'] = names['name'].str[-1]  # Extract last letter

# Pivot table for last letters
table = names.pivot_table(
    values='births',
    index='last_letter',
    columns=['sex', 'year'],
    aggfunc='sum'
)

# Filter data for specific years
subtable = table.loc[:, (slice(None), [1990, 2000, 2010])]
print("\nLast letter data for 1990, 2000, and 2010:")
print(subtable.head())

# Normalize data to calculate proportions
subtable_sum = subtable.sum()
letter_prop = subtable.div(subtable_sum, axis=1)

# Plot the popularity of last letters for males and females
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

colors = ['royalblue', 'seagreen', 'gold']  # Colors for different years

# Male last letter proportions
letter_prop['M'].plot(
    kind='bar',
    rot=0,
    ax=axes[0],
    title='Male Last Letter Proportions (1990, 2000, 2010)',
    color=colors
)

# Female last letter proportions
letter_prop['F'].plot(
    kind='bar',
    rot=0,
    ax=axes[1],
    title='Female Last Letter Proportions (1990, 2000, 2010)',
    color=colors
)

plt.tight_layout()
plt.show()

# Track popularity of last letters 'd', 'n', and 'y' for males over time
letter_prop_full = table.div(table.sum(), axis=1)  # Normalize full table
dny_ts = letter_prop_full.loc[['d', 'n', 'y'], 'M'].transpose()

print("\nProportions of names ending with 'd', 'n', and 'y' (male) over time:")
print(dny_ts.head())

# Plot changes over time
dny_ts.plot(
    figsize=(10, 6),
    title="Proportion of Male Names Ending in 'd', 'n', and 'y' Over Time",
    linewidth=2
)
plt.xlabel('Year')
plt.ylabel('Proportion')
plt.legend(title="Last Letter")
plt.grid()
plt.show()
