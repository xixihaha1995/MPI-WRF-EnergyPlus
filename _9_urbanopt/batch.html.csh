#!/bin/csh

#Cheyenne compile WRF script
#PBS -N batch
#PBS -A WYOM0106
#PBS -l walltime=00:30:00
#PBS -q premium
#PBS -j oe
#PBS -m abe
#PBS -M lwu4@uwyo.edu
#PBS -l select=1:ncpus=1

###Run real.exe
module load python/3.7.12
cd /glade/work/lichenwu/fortran_experiments/_9_urbanopt/
python3 ./lComparison.py >& batch.log