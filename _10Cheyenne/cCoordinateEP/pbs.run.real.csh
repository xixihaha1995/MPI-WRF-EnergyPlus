#!/bin/csh

#PBS -N lwu4_real
#PBS -A WYOM0106
#PBS -l walltime=00:02:00
#PBS -q economy
#PBS -j oe
#PBS -k eod
#PBS -l select=1

###Run
module load gnu/11.2.0
cd /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
mpiexec_mpt -spawn -np 1 ./real.exe

