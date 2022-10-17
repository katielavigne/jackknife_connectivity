# import packages
import pandas as pd

# define paths, files & variables
dpath = '/scratch/katie/ukbb/data/' # location to load glimfile & save outputs
dktvert_file = 'CIVET_2.0_DKT.txt' # DKT CIVET-based vertex file
dktinfo_file = 'DKT.csv' # DKT parcellation info
measure = 'thickness' # structural metric (e.g., thickness, surface_area, volume)

# read DKT and data files
df = pd.read_pickle(dpath + measure + '_vertexdata.pkl')
dktvert = pd.read_csv(dktvert_file, dtype=str, names=['roi'])
dktinfo = pd.read_csv(dktinfo_file, dtype=str)

# parcellation
parc = pd.DataFrame(index= df.index.copy())
for r in range(len(dktinfo)):
    roi = dktinfo.label_number[r]
    abr = dktinfo.abbreviation[r]
    means = pd.DataFrame(df.iloc[:,dktvert.index[dktvert.roi == roi]].mean(axis=1),columns=[abr], index= df.index.copy())
    parc = pd.concat([parc,means], axis = 1)

# write to csv
parc.to_csv(dpath + 'dkt_parcellation_' + measure + '.csv') # parcellated data