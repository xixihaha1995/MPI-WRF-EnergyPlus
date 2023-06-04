#!/bin/csh

#Cheyenne real.exe script
#PBS -N lwu4_real
#PBS -A WYOM0106
#PBS -l walltime=00:03:00
#PBS -q economy
#PBS -j oe
##PBS -m abe
##PBS -M lwu4@uwyo.edu
#PBS -l nodes=1:ppn=4

###Run real.exe
cd /glade/work/lichenwu/NWP/WRF/test/em_real
mpiexec_mpt dplace -s 4 ./real.exe