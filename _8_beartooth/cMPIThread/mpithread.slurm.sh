#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:01:00
#SBATCH --job-name=test_lw
#SBATCH --output=test_lw%j.out
#SBATCH --error=test_lw%j.err

# Set the directory where you want to install the software, Change to the source code directory
DIR="/home/lwu4/fortran_experiments/_8_beartooth/cMPIThread"
cd $DIR
pwd
make
echo "Running on $(hostname)"
# Execute the program
mpirun -np 4 ./mpi_thread_funneled_example
make clean
