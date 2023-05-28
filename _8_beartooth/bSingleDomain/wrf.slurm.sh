#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=test_lw
#SBATCH --output=test_lw%j.out
#SBATCH --error=test_lw%j.err

# Set the directory where you want to install the software, Change to the source code directory
DIR="/project/communitybem/NWP/WRF/test/em_real"
cd $DIR
pwd
echo "Running on $(hostname)"
# Execute the program
mpirun ./wrf.exe
