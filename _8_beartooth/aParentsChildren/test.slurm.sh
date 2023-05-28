#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:05:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=3
#SBATCH --job-name=configure_script
#SBATCH --output=configure_script_%j.out
#SBATCH --error=configure_script_%j.err

# Load the required module
# module purge
# module load arcc/1.0
# module load gcc/11.2.0

# Set the directory where you want to install the software
DIR="~/fortran_experiments/_8_beartooth/aParentsChildren"

# Change to the source code directory
cd $DIR
pwd
make
mpirun ./parent.exe
