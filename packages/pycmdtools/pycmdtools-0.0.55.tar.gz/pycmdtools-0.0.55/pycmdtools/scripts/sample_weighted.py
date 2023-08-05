import csv

import numpy as np
import pandas as pd

from unidecode import unidecode

old_df = pd.read_csv(
    'old_queries.txt',
    sep='\t',
    quotechar=None,
    names=['query'],
    quoting=csv.QUOTE_NONE,
    encoding='utf8'
)
df = pd.read_csv(
    'all_actual_queries.txt',
    sep='\t',
    quotechar=None,
    names=['query'],
    quoting=csv.QUOTE_NONE,
    encoding='utf8'
)
df['query'] = df['query'].apply(unidecode)
df['query'] = df['query'].str.replace(r'\s{2,}', ' ').str.strip().str.lower()
df = df.loc[~df['query'].isin(old_df['query'])]

df = df.groupby('query', sort=False).size()
df.sample(
    n=12000,
    weights=np.log2(df) / np.log2(df).sum()).index.to_series().to_csv('sample.txt', sep='\t', index=False)
