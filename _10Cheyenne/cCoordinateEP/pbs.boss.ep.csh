#!/bin/csh

#PBS -N lwu4_parent_ep
#PBS -A WYOM0106
#PBS -l walltime=00:03:00
#PBS -q economy
#PBS -j oe
#PBS -k eod
#PBS -l select=1:mpiprocs=10

cat $PBS_NODEFILE
set nbr_parent = 1
###Run
cd /glade/u/home/lichenwu/project/fortran_experiments/_10Cheyenne/cCoordinateEP
module load gnu/11.2.0
make
mpiexec_mpt -spawn -np $nbr_parent ./mpi_app
make clean

