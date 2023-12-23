#%%
import pandas as pd
import numpy as np
from datetime import datetime as dt
from modules.read_map import read_map
from modules.mapit import mapit
import jellyfish  # approximate match

def convert(file,
            col_rename=['Account', 'Budget', 'Source_of_Funds', 'Recurring', 'Budget_old', 'Current_Balance', 'Difference', 'Comments'],
            budget_columns=[1,4],
            year=2024,
            col_out   =['Year', 'Description', 'InOrOut', 'AccountNum', 'Account', 'Budget', 'File']):
    ## READ OFFICE VERSION OF BUDGET DATA INTO DATAFRAME: df

    ## read budget file and fix column names
    df = pd.read_excel('input_files/' + file)
    df.columns = col_rename

    ## remove any row where Source_of_Funds is NaN
    df = df.dropna(subset = ['Source_of_Funds'])

    ## create another column with budget line item number only because database not consistent with descriptions
    df['AccountNum'] = df.Account.str.extract('(^\d+a|^\d+)')
    df['AccountNum'] = pd.to_numeric(df['AccountNum'])
    ## type(df.iloc[0]['AccountNum'])

    ## create column indicating whether account is income (In) or expense (Out)
    df['InOrOut'] = np.where(df['AccountNum'] < 5000, 'In', 'Out')
    df['AccountNum'] = df['AccountNum'].apply(str) # convert back to string for merge later
    for i in budget_columns:
        df.iloc[:,i] = np.where(df['InOrOut'] == 'In', df.iloc[:,i], -df.iloc[:,i])

    ## add year and Description columns
    df['Year'] = year
    ## df['Description'] = dt.today().strftime('%Y-%m-%d')
    today = dt.today().strftime('%m/%d/%y')
    ## df['Description'] = dt.strptime(today, '%m/%d/%y')
    df['Description'] = 'Budget ' + str(year) + ' (' + today + ')'

    ## add file name column
    df['File'] = file

    ## move InOrOut and AccountNum to front of dataframe
    df = df[col_out]

    return df


#%%
## read prior years
df = pd.read_excel('input_files/budget_all.xlsx')
df = df.drop('Account (map)', axis=1)
df = df.drop('Match Level', axis=1)
#df = df.drop('Category', axis=1)
#df = df.drop('SourceOfFunds', axis=1)

## ## available columns
## ## df = df[['Index', 'Year', 'Description', 'InOrOut', 'AccountNum', 'Account (budget)',
## ##          'Account (map)', 'Match Level', 'Budget', 'Category', 'SourceOfFunds']]
## df = df[['Year', 'Description', 'InOrOut', 'AccountNum', 'Account (map)', 'Budget', 'File']]

## ## rename
## df.columns = ['Year', 'Description', 'InOrOut', 'AccountNum', 'Account', 'Budget', 'File (budget)']

#%%


#%%

file = []
file.append('budget_2024_office_2023_11_15.xlsx')
file.append('budget_2024_dave_2023_11_16.xlsx')

file = 'budget_2024_dave_2023_11_17.xlsx'
file = 'budget_2024_dave_2023_11_19.xlsx'
file = 'budget_2024_dave_2023_11_16xx.xlsx'
file = 'budget_2024_office_2023_11_15_plus40k.xlsx'
file = 'budget_2024_office_2023_12_20.xlsx'

# read each office formatted budget file and combine with df
if type(file) == str:
    budget = convert(file)
    df = pd.concat([df, budget], axis=0)
else:
    for i in range(0,len(file)):
        budget = convert(file[i])
        df = pd.concat([df, budget], axis=0)

#%% 
## map to categories
map, map_duplicates = read_map(sheet='2024')

#%%
## first need to convert AccountNum to string for merge operation
df['AccountNum'] = df['AccountNum'].apply(str)
dfmapped, missing = mapit(df, map)

#%%
## drop and rename columns from: 
dfmapped = dfmapped.drop('InOrOut_x', axis=1)
dfmapped.rename(columns = {"Account_x": "Account (budget)"}, inplace = True) 
dfmapped = dfmapped.drop('InOrOut_y', axis=1)
dfmapped.rename(columns = {"Account_y": "Account (map)"}, inplace = True) 


#%%
## Check actual for mismatched account names
mismatched_dict = []
for row in range(len(dfmapped)):
    a = jellyfish.jaro_distance(str(dfmapped.loc[row,'Account (budget)']), str(dfmapped.loc[row,'Account (map)']))    # approximate match
    mismatched_dict.append(a)
dfmapped['Match Level'] = mismatched_dict

#%%
## ## reorder and keep selected columns
## dfmapped['Index'] = list(range(1,len(dfmapped)+1))
## dfmapped = dfmapped[['Index', 'Year', 'Description', 'InOrOut', 'AccountNum', 'Account (budget)', 'Account (map)', 'Match Level', 'Budget', 'Category', 'SourceOfFunds', 'Purpose', 'InternalExternal', 'File (budget)']]


# %%
## reorder specific columns but keep all columns
allcols = list(dfmapped)
## first = ['Year', 'Description', 'InOrOut', 'AccountNum', 'Account (budget)', 'Budget', 'Category', 'SourceOfFunds', 'Purpose', 'InternalExternal', 'File']
first = ['Year', 'Description', 'InOrOut', 'AccountNum', 'Account (budget)', 'Account (map)', 'Match Level', 'Budget', 'Category', 'SourceOfFunds', 'File']
first = ['Year', 'Description', 'InOrOut', 'AccountNum', 'Account (budget)', 'Account (map)', 'Match Level', 'Budget', 'File']
rest = [i for i in allcols if i not in first]
dfmapped_new = pd.concat([dfmapped[first],dfmapped[rest]], axis=1)
dfmapped = dfmapped_new


# %%
## write to Excel
dfmapped.to_excel('compare_out.xlsx', index=False)


#%%
##################################################

##%%
### read prior year
#import pandas as pd
#df = pd.read_excel('input_files/budget_2023.xlsx')
#df = df[['Account', 'Budget']]
#
##%%
#df['AccountNum'] = df.Account.str.extract('(^\d+a|^\d+)')
#df.columns = ['Account_2023', 'Budget_2023', 'AccountNum']
#
#
##%%
### merge dataframes (must be on sring)
#dfnew = pd.merge(df, budget, how='outer', on='AccountNum')
#dfnew = [['InOrOut', 'AccountNum', 'Account', 'Budget_2024', 'Account_2023', 'Budget_2023']]


# %%
