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

only_devs_list =  ['developer', 'engineer']
only_devs = df1.loc[df1['title'].str.contains('|'.join(only_devs_list), case=False, na=False)]
only_devs = only_devs.groupby(['companyName']).size().reset_index(name='counts')

rhs = only_devs
# rhs['Contains string'] = (df['companyName'].apply(lambda x: x.str.contains(df.companyName))).sum(axis=1)

rhs = (df.companyName
          .apply(lambda x: only_devs[only_devs.companyName.str.find(x).ge(0)]['counts'])
        #   .apply(lambda x: only_devs.companyName.str.contains(x)).sum(axis=1)
          .bfill(axis=1)
          .iloc[:, 0])

rhs = (pd.concat([df.companyName, rhs], axis=1, ignore_index=True)
 .rename(columns={0: 'companyName', 1: 'count'}))

# print(rhs)
# only_devs.to_csv('yeboi2.csv')

only_talent_list =  ['human', 'recruiter', 'talent']
contains_talent = df1.loc[df1['title'].str.contains('|'.join(only_talent_list), case=False, na=False)]
contains_talent['talent'] = 1

contains_talent = contains_talent.groupby(['companyName'])['talent'].sum().reset_index(name="talentCount")

contains_talent = (df.companyName
          .apply(lambda x: contains_talent[contains_talent.companyName.str.find(x).ge(0)]['talentCount'])
          .bfill(axis=1)
          .iloc[:, 0])

contains_talent = (pd.concat([df.companyName, contains_talent], axis=1, ignore_index=True)
 .rename(columns={0: 'companyName', 1: 'talentCount'}))

final = pd.merge(df, contains_cto[['companyName', 'cto', 'fullName', 'title', 'cofounder']],on='companyName', how='left')
final = pd.merge(final, rhs[['companyName', 'count']],on='companyName', how='left')
final = pd.merge(final, contains_talent[['companyName', 'talentCount']],on='companyName', how='left')

final['Person name'] = final['fullName']
final['Role (LI)'] = final['title']
final['Also Cofounder?'] = final['cofounder']

final.loc[final['count'].isnull(), 'count'] = 0
final['count'] = final['count'].astype('int')
final['How many devs do they have on LI'] = final['count']

final.loc[final['talentCount'].isnull(), 'talentCount'] = 0
final['talentCount'] = final['talentCount'].astype('int')
final.loc[final['talentCount'] > 0, 'Anyone in Talent Aquisition?'] = True
final.loc[final['talentCount'] == 0, 'Anyone in Talent Aquisition?'] = False

final = final.assign(result=final['Person name'].isin(df2['fullName']).astype(int))
final.loc[final['result'] == 1, 'Delta LI Follower'] = True
final.loc[final['result'] == 0, 'Delta LI Follower'] = False

final['Do they have a CTO on LI'] = final['cto']
final.loc[final['cto'] != True, 'Do they have a CTO on LI'] = False

final.drop(['cto', 'fullName', 'result', 'title', 'cofounder', 'count', 'talentCount'], axis=1, inplace=True)

final.to_csv('yeboi.csv')
