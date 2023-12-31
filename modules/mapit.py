# %%
def mapit(dfin, map):
    '''
    pd.merge(dfin, map, how='left', on='AccountNum')

    first need to drop any columns from dfin that I want taken from the map instead of the source files
    '''

    import pandas as pd
    import regex as re

    df = dfin.copy()

    ## drop columns from df that should come from map instead
    #dfnames = list(df)
    #mapnames = list(map)
    #allnames = dfnames + mapnames
    #dups = list({x for x in allnames if allnames.count(x) > 1})
    #
    #for i in range(0,len(mapnames)):
    #    budget = convert(file[i])
    #    df = pd.concat([df, budget], axis=0)
    #
    #df = df.drop('InOrOut', axis=1)
    #df = df.drop('Category', axis=1)
    #df = df.drop('Purpose', axis=1)
    #df = df.drop('SourceOfFunds', axis=1)

    df = pd.merge(df, map, how='left', on='AccountNum')

    ## create InOrOut column if it does not exist
    ## because it was in both df and map so merge created _x and _y copies
    df['InOrOut'] = df.get('InOrOut', df['InOrOut_y']) 

    ## flag any line items from dfin that are not in the map (e.g., so no Category assigned)
    nan_values = df[df['Category'].isna()]
    if len(nan_values) != 0:
    #    print('')
    #    print('FATAL ERROR: Following budget entries are missing a Category assignment in map.xlsx file')
    #    print(nan_values)
    #    sys.exit()

        ## classify anything that does not have Category defined in map
        mask = df['Category'].isna()
        df.loc[mask, 'Category'] = 'Xbudget'
        df.loc[mask, 'SourceOfFunds'] = 'Xbudget'
       
        ## if Account is missing from map, replace it with Account from dataframe
        if 'Account' in df:
            df.loc[df['Account'].isna(), 'Account'] = df['AccountNum']
        if 'Account_x' in df:
            df.loc[df['Account_x'].isna(), 'Account_x'] = df['AccountNum']
        if 'Account_y' in df:
            df.loc[df['Account_y'].isna(), 'Account_y'] = df['AccountNum']

        ## ## set InOrOut based on dollar fields being positive or negative
        ## dollarfields = [x for x in df.columns if re.findall(r'Amount',x)]
        ## df['dollarsum'] = 0   # initialize new variable
        ## for i in dollarfields:
        ##     df.loc[mask, 'dollarsum'] = df.loc[mask, 'dollarsum'] + df.loc[mask, i]
        ## df.loc[(df.InOrOut.isna()) & (df.dollarsum >= 0), 'InOrOut'] = 'In' 
        ## df.loc[(df.InOrOut.isna()) & (df.dollarsum <  0), 'InOrOut'] = 'Out' 

    return df, nan_values


#import pandas as pd
#df = pd.DataFrame({"A" : [14, 4, 5, 4, 1],
#                   "AccountNum" : ['100', '200', '300', '400', '500'],
#                   "Amount" : [1,2,-3,-4,-5],
#                   "Amounta" : [2,3,-1,-1,-1]})
#map = pd.DataFrame({"InOrOut" : ['In', 'Out'],
#                    "Category" : ['asdf', 'jkl;'],
#                    "SourceOfFunds" : ['end', 'cov'],
#                    "Account" : ['200 some income', '300 some expense'],
#                    "AccountNum" : ['200', '300'] })
#out, junk = mapit(df,map)
#out

# %%
