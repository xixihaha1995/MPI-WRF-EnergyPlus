#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:01:00
#SBATCH --partition=teton
#SBATCH --nodes=1
##SBATCH --ntasks-per-node=3
#SBATCH --job-name=configure_script
#SBATCH --output=configure_script_%j.out
#SBATCH --error=configure_script_%j.err

# Load the required module
# module purge
# module load arcc/1.0
# module load gcc/11.2.0

# Set the directory where you want to install the software, Change to the source code directory
echo "Running on processor:"
echo $HOSTNAME
echo $SLURM_JOB_NODELIST