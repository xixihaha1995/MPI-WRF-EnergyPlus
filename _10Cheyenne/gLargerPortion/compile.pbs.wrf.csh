#!/bin/csh

#Cheyenne compile WRF script
#PBS -N lwu4_com_WRF
#PBS -A WYOM0106
#PBS -l walltime=00:30:00
#PBS -q premium
#PBS -j oe
#PBS -m abe
#PBS -M lwu4@uwyo.edu
#PBS -l select=1:ncpus=10

###Run real.exe
module load gnu/11.2.0
cd /glade/work/lichenwu/NWP/WRF/
./compile em_real -j 10 >& compile.log