import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

df = pd.read_csv('final.csv')
df1 = pd.read_csv('result.csv')

exclude_list = ['director', 'assistant', 'instructor', 'actor']
excludes_df = df1.loc[~df1['title'].str.contains('|'.join(exclude_list), case=False, na=False)]

contains_cto = excludes_df.loc[excludes_df['title'].str.contains('cto', case=False, na=False)]
contains_cto['cto'] = True

final = pd.merge(df, contains_cto[['companyName', 'cto']],on='companyName', how='left')

final['Do they have a CTO on LI'] = final['cto']
final.loc[final['cto'] != True, 'Do they have a CTO on LI'] = False

final.drop(['cto'], axis=1, inplace=True)

final.to_csv('yeboi.csv')

