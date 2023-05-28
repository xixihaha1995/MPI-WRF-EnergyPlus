#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH --job-name=test_lw
#SBATCH --output=test_lw%j.out
#SBATCH --error=test_lw%j.err

# Set the directory where you want to install the software, Change to the source code directory
DIR="/home/lwu4/fortran_experiments/_8_beartooth/aParentsChildren"
cd $DIR
pwd
make
# Execute the program
mpirun -verbose -np 1 ./parent.exe
