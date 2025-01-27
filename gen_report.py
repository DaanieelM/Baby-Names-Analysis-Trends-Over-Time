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
 

