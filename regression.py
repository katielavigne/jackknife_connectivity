# import packages
import os
import pandas as pd
import statsmodels.formula.api as sm

# define paths, files & variables
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
gfile = 'ukbb_glimfile_final.csv' # glimfile
measure = 'thickness' # structural metric (e.g., thickness, surface_area, volume)
idvar = 'eid' # unique subject ID variable
covars = ['age','mean_' + measure] # covariates
group = 'dx' # grouping variable (if applicable)

# read files
glim = pd.read_csv(dpath + gfile, index_col='eid', dtype={'eid':str})
parc = pd.read_csv(dpath + 'dkt_parcellation_' + measure + '.csv', index_col='eid', dtype={'eid':str})
mean_measure = pd.read_csv(dpath + 'mean_' + measure + '.csv', index_col='eid', dtype={'eid':str})
glim = glim[glim.index.isin(parc.index)]

# merge glimfile and parcellated data
glim = glim.join(mean_measure) # merge glim & mean thickness # modify to total_measure if using surface_area
glim_parc = glim.join(parc) # join glim + mean thickness & parcellated data
rois = parc.columns

# regression
if group in glim_parc.columns: # group-based regressions if applicable
    for g in glim_parc[group].unique():
        resid=[]
        glim_parc_group = glim_parc[glim_parc[group]==g]
        parc_group = glim_parc_group[rois]
        covar1 = glim_parc_group[covars[0]]
        covar2 = glim_parc_group[covars[1]]
        for i in parc_group:
            reg = sm.ols('parc_group.loc[:,i] ~ covar1 + covar2', data=glim_parc_group).fit()
            residuals = reg.resid
            resid.append(residuals)
        
        # merge groups
        if g == glim_parc[group].unique()[0]:
            res = pd.DataFrame(resid).T
            res.columns = parc.columns
        else:
            tmp = pd.DataFrame(resid).T
            tmp.columns = parc.columns
            res = pd.concat([res,tmp], sort=True)
else:
    resid=[]
    covar1 = glim_parc[covars[0]]
    covar2 = glim_parc[covars[1]]
    for i in parc:
        reg = sm.ols('parc.loc[:,i] ~ covar1 + covar2', data=glim_parc).fit()
        residuals = reg.resid
        resid.append(residuals)
    res = pd.DataFrame(resid).T
    res.columns = parc.columns

# write to csv
glim.to_csv(dpath + 'glimfile.csv')
glim_parc.to_csv(dpath + 'glimfile_parcellation.csv')
res.to_csv(dpath + 'residuals.csv')