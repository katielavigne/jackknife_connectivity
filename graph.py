# import packages
import pandas as pd
import numpy as np 
import bct

# define paths, files & variables
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
idvar = 'eid' # unique subject ID variable
group = 'dx' # grouping variable (if applicable)

# read files
glim = pd.read_csv(dpath + 'glimfile.csv', index_col=[idvar], dtype={'eid':str})

# compute graph measures
if group in glim.columns:
    for g in glim[group].unique():
        glim_group = glim[glim[group]==g]
        jk = np.load(dpath +'jackknife_output_group_' + str(g) + '.npy')
        
        # fixing that the diagonals are all 0 
        for i in jk:
            np.fill_diagonal(i, 0, wrap=True)
        
        # strengths
        def strengths_und(jk):
            return np.sum(jk, axis=1)
        strengths = strengths_und(jk)
        s = pd.DataFrame(data=strengths, index=glim_group.index.copy())
        s.columns = ['Strength_'+ str(i) for i in range(1, s.shape[1] + 1)]
        tmp = glim_group.join(s)
        
        # global efficiency
        globeff = []
        for i in jk:
            bct.efficiency_wei(i)
            globeff.append(bct.efficiency_wei(i))
        e = pd.DataFrame(data=globeff, index=glim_group.index.copy())
        e.columns = ['Global Efficiency']
        tmp = tmp.join(e)
    
        # merge groups
        if g == glim[group].unique()[0]:
            data_conn = tmp
        else:
            data_conn = pd.concat([data_conn,tmp])
    
    # write to csv
    data_conn.to_csv(dpath + 'glimfile_jackknife_output.csv')
else:
    jk = np.load(dpath + 'jackknife_output.npy')
    
    # fixing that the diagonals are all 0
    for i in jk:
        np.fill_diagonal(i, 0, wrap=True)
    
    # strengths
    def strengths_und(jk):
        return np.sum(jk, axis=1)
    strengths = strengths_und(jk)
    s = pd.DataFrame(data=strengths, index=glim.index.copy())
    s.columns = ['Strength_'+str(i) for i in range(1, s.shape[1] + 1)]
    data_conn = glim.join(s)
    
    # global efficiency
    globeff = []
    for i in jk:
        bct.efficiency_wei(i)
        globeff.append(bct.efficiency_wei(i))
    e = pd.DataFrame(data=globeff, index=glim.index.copy())
    e.columns = ['Global Efficiency']
    data_conn = data_conn.join(e)
    
    # write to csv
    data_conn.to_csv(dpath + 'glimfile_jackknife_output.csv')