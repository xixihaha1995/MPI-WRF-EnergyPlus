#!/bin/bash
#SBATCH --account=communitybem
#SBATCH --job-name=configure_script
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --output=configure_script_%j.out
#SBATCH --error=configure_script_%j.err

# Load the required module
module purge
module load arcc/1.0
module load gcc/11.2.0

# Set the directory where you want to install the software
DIR="/project/communitybem/Build_WRF/LIBRARIES"

# Change to the source code directory
cd /project/communitybem/downloads/netcdf-fortran-4.5.2
pwd
# Run the configure script
./configure --prefix="$DIR/netcdf"
make 
make install
# Optionally, you can add additional commands here, such as make and make install
module unload arcc/1.0
# Submit the job to the SLURM scheduler

configure:4667: /apps/u/spack/gcc/8.5.0/gcc/11.2.0-vjgyill/bin/gcc -c -g -O2 -I/project/communitybem/Build_WRF/LIBRARIES/grib2/include -I/project/communitybem/Build_WRF/LIBRARIES/curl/include -I/project/communitybem/Build_WRF/LIBRARIES/netcdf/include conftest.c >&5
conftest.c: In function 'main':
conftest.c:20:7: error: unknown type name 'choke'
   20 |       choke me

