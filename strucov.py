# import packages
import pandas as pd

# define paths, files & variables
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
gfile = 'ukbb_glimfile_final.csv' # glimfile
idvar = 'eid' # unique subject ID variable
group = 'dx' # grouping variable (if applicable)

# read files
glim_parc = pd.read_csv(dpath + 'glimfile_parcellation.csv', index_col=[idvar], dtype={'eid':str})
res = pd.read_csv(dpath + 'residuals.csv', index_col=[idvar], dtype={'eid':str}) # read residuals
    
# full sample (or group) correlation matrix
if group in glim_parc.columns:
    for g in glim_parc[group].unique():
        res_group = res.loc[glim_parc[group]==g]
        corrmtrix = res_group.corr(method='pearson')
        corrmtrix.to_csv(dpath + 'corrmtrix_full_group_' + str(g) + '.csv') # write to csv
else:
    corrmtrix = res.corr(method='pearson')
    corrmtrix.to_csv(dpath + 'corrmtrix_full.csv') # write to csv