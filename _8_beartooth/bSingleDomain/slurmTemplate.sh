#!/bin/bash
#SBATCH --account=communitybem
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --job-name=configure_script
#SBATCH --output=configure_script_%j.out
#SBATCH --error=configure_script_%j.err

# Load the required module
# module purge
# module load arcc/1.0
# module load gcc/11.2.0

# Set the directory where you want to install the software
DIR="/project/communitybem/Build_WRF/LIBRARIES"

# Change to the source code directory
cd /project/communitybem/downloads/netcdf-fortran-4.5.2
pwd
# Run the configure script
./configure --prefix="$DIR/netcdf"
# Optionally, you can add additional commands here, such as make and make install
make 
make install
# Submit the job to the SLURM scheduler
