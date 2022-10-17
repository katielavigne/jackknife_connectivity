# import packages
import pandas as pd
import numpy as np 

# define paths, files & variables
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
idvar = 'eid' # unique subject ID variable
group = 'dx' # grouping variable (if applicable)

# read files
glim_parc = pd.read_csv(dpath + 'glimfile_parcellation.csv', index_col=[idvar], dtype={'eid':str})
res = pd.read_csv(dpath + 'residuals.csv', index_col=[idvar], dtype={'eid':str})

# jackknife correlation 
if group in glim_parc.columns:
    for g in glim_parc[group].unique():
        glim_parc_group = glim_parc[glim_parc[group]==g]
        res_group = res.loc[glim_parc[group]==g]
        corrmtrix = pd.read_csv(dpath + 'corrmtrix_full_group_' + str(g) + '.csv', index_col=[0])
        jack = []
        n = len(glim_parc_group[:]) # full sample
        for i,row in res_group.iterrows(): # i = eid, so the loop goes over each row in the dataframe meaning each participant
            LOO = res_group.drop(i) # and drops one row depending on i per loop (LOO = leave one out)
            corrLOO = LOO.corr(method='pearson');
            W = (n*corrmtrix)-((n-1)*corrLOO);
            # Absolute
            normW = abs(W);
            jack.append(normW)
        jk = np.array(jack)
        np.save(dpath + 'jackknife_output_group_' + str(g) + '.npy', jk) # write out as numpy array
else:
    jack = []
    n = len(glim_parc[:]) # full sample
    corrmtrix = pd.read_csv(dpath + 'corrmtrix_full.csv', index_col=[0])
    for i,row in res.iterrows(): # i = eid, so the loop goes over each row in the dataframe meaning each participant
        LOO = res.drop(i) # and drops one row depending on i per loop (LOO = leave one out)
        corrLOO = LOO.corr(method='pearson'); 
        W = (n*corrmtrix)-((n-1)*corrLOO);
        # Absolute
        normW = abs(W);
        jack.append(normW)
    jk = np.array(jack)
    np.save(dpath + 'jackknife_output.npy', jk) # write out as numpy array