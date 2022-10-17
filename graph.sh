#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --mem=186G
#SBATCH --account=def-mlepage
#SBATCH --job-name=graph
#SBATCH --output=/scratch/katie/ukbb/logs/%x-%j.out
#SBATCH --error=/scratch/katie/ukbb/logs/%x-%j.err

# command: sbatch --dependency=afterok:$jid5 jackknife.sh

# load modules
module load python/3.8

# create virtual environment
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

# install packages
# (see https://docs.alliancecan.ca/wiki/Python#Creating_virtual_environments_inside_of_your_jobs for creating requirements.txt)
pip install --no-index --upgrade pip
pip install --no-index -r requirements.txt

python graph.py
