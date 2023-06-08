#!/bin/csh

#PBS -N lwu4_com_wrf
#PBS -A WYOM0106
#PBS -l walltime=00:30:00
#PBS -q economy
#PBS -j oe
#PBS -k eod
#PBS -l select=1:mpiprocs=30

###Run
cd /glade/u/home/lichenwu/project/NWP/WRF
module load gnu/11.2.0
./clean -a
./configure
34
1
./compile em_real -j 30 >& log.compile