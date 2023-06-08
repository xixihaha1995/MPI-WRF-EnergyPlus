#!/bin/csh

#PBS -N lwu4_wrf_ep
#PBS -A WYOM0106
#PBS -l walltime=00:15:00
#PBS -q economy
#PBS -j oe
#PBS -k eod
#PBS -l select=2:mpiprocs=36

cat $PBS_NODEFILE
set nbr_parent = 1
###Run
# cd /glade/u/home/lichenwu/project/fortran_experiments/_10Cheyenne/cCoordinateEP
module load gnu/11.2.0
# make
## cp -r resources /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
# cp child.exe /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
cd /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
mpiexec_mpt -spawn -np $nbr_parent ./wrf.exe >& /glade/scratch/lichenwu/ep_temp/log.energyplus

