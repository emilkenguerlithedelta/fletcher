import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

df = pd.read_csv('final.csv')
df1 = pd.read_csv('result.csv')
df2 = pd.read_csv('followers.csv')

exclude_list = ['director', 'assistant', 'instructor', 'actor']
excludes_df = df1.loc[~df1['title'].str.contains('|'.join(exclude_list), case=False, na=False)]

contains_cto = excludes_df.loc[excludes_df['title'].str.contains('cto', case=False, na=False)]
contains_cto['cto'] = True
contains_cto['cofounder'] = False

contains_cto.loc[contains_cto['title'].str.contains('founder', case=False, na=False) == True, 'cofounder'] = True

final = pd.merge(df, contains_cto[['companyName', 'cto', 'fullName', 'title', 'cofounder']],on='companyName', how='left')

final['Person name'] = final['fullName']
final['Role (LI)'] = final['title']
final['Also Cofounder?'] = final['cofounder']

final = final.assign(result=final['Person name'].isin(df2['fullName']).astype(int))
final.loc[final['result'] == 1, 'Delta LI Follower'] = True
final.loc[final['result'] == 0, 'Delta LI Follower'] = False

final['Do they have a CTO on LI'] = final['cto']
final.loc[final['cto'] != True, 'Do they have a CTO on LI'] = False

final.drop(['cto', 'fullName', 'result', 'title'], axis=1, inplace=True)

final.to_csv('yeboi.csv')
