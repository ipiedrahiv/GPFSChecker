# GPFSChecker

Simple tool to provide user insights on GPFS projects storage usage.

After the sbatch job completes its execution, check slurm job output to review:


- Your oldest directories

- Your largest files

- Directories in projects without group write permissions

- Subdirectories within your project space where you do not have write permission.

Launch with `sbatch --account=<ACCOUNT> finder.sh <SEARCH_DIRECTORY>`
