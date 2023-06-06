#!/bin/csh

#Cheyenne wrf.exe script
#PBS -N lwu4_wrf
#PBS -A WYOM0106
#PBS -l walltime=01:00:00
#PBS -q regular
#PBS -j oe
#PBS -l select=1:ncpus=1:mpiprocs=1

###Run real.exe
cd /glade/work/lichenwu/NWP/WRF/test/em_real
mpiexec_mpt dplace -s 1 ./wrf.exe