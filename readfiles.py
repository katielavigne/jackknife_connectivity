# import packages
import os, glob
import pandas as pd

# define paths, files & variables
civpath = '/scratch/katie/ukbb/data/civet_0mm/' # location containing civet outputs
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
measure = 'thickness' # structural metric (e.g., thickness, surface_area, volume)
idvar = 'eid' # unique subject ID variable

if not os.path.exists(dpath + measure + '_vertexdata.pkl'):
    # find files & IDs
    Lfiles = glob.glob(civpath + '*left*')
    Lfiles.sort()
    Rfiles = glob.glob(civpath + '*right*')
    Rfiles.sort()
    subjIDs = [ids.split('/')[-1].split('_')[1] for ids in Lfiles] # modify this for different filename conventions

    # make dataframe & save as pickle
    Ldf = pd.concat((pd.read_csv(Lf, dtype=float, header=None).T for Lf in Lfiles))
    Rdf = pd.concat((pd.read_csv(Rf, dtype=float, header=None).T for Rf in Rfiles))
    df = pd.concat([Ldf,Rdf], axis=1)
    df.index = subjIDs
    df.index.names = [idvar]
    df.to_pickle(dpath + measure + '_vertexdata.pkl')

    # calculate and save mean anatomical measure (mean thickness)
    mean_measure = pd.DataFrame(pd.to_numeric(df.mean(axis=1)), columns=['mean_' + measure])
    mean_measure.to_csv(dpath + 'mean_' + measure + '.csv')

    # calculate and save total anatomical measure (total thickness)
    tot_measure = pd.DataFrame(pd.to_numeric(df.sum(axis=1)), columns=['total_' + measure])
    tot_measure.to_csv(dpath + 'total_' + measure + '.csv')