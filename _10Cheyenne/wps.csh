#!/bin/csh

#Cheyenne wps script
#PBS -N lwu4_wps
#PBS -A WYOM0106
#PBS -l walltime=00:03:00
#PBS -q economy
#PBS -j oe
##PBS -m abe
##PBS -M lwu4@uwyo.edu
#PBS -l select=1:ncpus=1:mpiprocs=1

###Run WPS
cd /glade/work/lichenwu/NWP/WPS
mpiexec_mpt dplace -s 1 ./geogrid.exe >& geogrid.log