#!/bin/bash

#SBATCH --job-name=space_summary
#SBATCH --chdir=.
#SBATCH --qos=gp_debug
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=slurm_output/result_%j.out
#SBATCH --error=slurm_output/result_%j.err

SEARCH_PATH=$1

if [ -z "$SEARCH_PATH" ]; then
  echo "Error: SEARCH_PATH not provided"
  exit 1
fi

module load hdf5/1.14.1-2
module load python/3.8.18-gcc

echo $SEARCH_PATH

find $SEARCH_PATH -mindepth 2 -maxdepth 6 -xdev -type d -user $USER -printf '%M,%u,%TY-%Tm-%Td,%s,%p\n' 2>/dev/null > slurm_output/find_output.csv

python analyze.py
