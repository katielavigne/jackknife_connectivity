#!/bin/bash
# Code for running jackknife connectivity on morphometric brain measures (cortical thickness, surface_area, volume) using high-performance computing. Run on the Béluga cluster via Calcul Québec & the Digital Research Alliance of Canada (formerly Compute Canada).

# make logfile directory
mkdir -p $SCRATCH/ukbb/logs

# read files
jid1=$(sbatch --parsable readfiles.sh)

# parcellation
jid2=$(sbatch --parsable --dependency=afterok:$jid1 parcellation.sh)

# regression
jid3=$(sbatch --parsable --dependency=afterok:$jid2 regression.sh)

# structural covariance
jid4=$(sbatch --parsable --dependency=afterok:$jid3 strucov.sh)

# jackknife
jid5=$(sbatch --parsable --dependency=afterok:$jid4 jackknife.sh)

# graph theory
jid6=$(sbatch --parsable --dependency=afterok:$jid5 graph.sh)

sleep 5
sq
