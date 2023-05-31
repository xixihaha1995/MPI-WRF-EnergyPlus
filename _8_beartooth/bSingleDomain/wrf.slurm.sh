#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:10:00
#SBATCH --nodes=4
#SBATCH --mem=6G
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=test_lw
#SBATCH --output=test_lw%j.out
#SBATCH --error=test_lw%j.err

# Set the directory where you want to install the software, Change to the source code directory
module load arcc/1.0
module load gcc/12.2.0
module load zlib/1.2.12
module load openmpi/4.1.4
EXECDIR="/project/communitybem/NWP/WRF/test/em_real"
cd $EXECDIR
pwd
echo "Running on $(hostname)"
# Execute the program
srun ./wrf.exe
