#!/bin/csh

#PBS -N lwu4_wrf_ep
#PBS -A WYOM0106
#PBS -l walltime=00:02:00
#PBS -q regular
#PBS -j oe
#PBS -k eod
#PBS -l select=10:mpiprocs=1

cat $PBS_NODEFILE
set nbr_parent = 2
###Run
# cd /glade/u/home/lichenwu/project/fortran_experiments/_10Cheyenne/cCoordinateEP
module load gnu/11.2.0
# make
## cp -r /glade/u/home/lichenwu/project/fortran_experiments/_9_urbanopt/resources-22-2-0  /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
## cp -r /glade/u/home/lichenwu/project/fortran_experiments/_6_Coordinate_EP/j7080/python_standard_lib /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
## cp saved.module_sf_bep_bem.F  /glade/u/home/lichenwu/project/NWP/WRF/phys/module_sf_bep_bem.F
# cp -f child.exe /glade/u/home/lichenwu/project/NWP/WRF/test/em_real/
cd /glade/u/home/lichenwu/project/fortran_experiments/_10Cheyenne/eIntraInter
pwd
mpiexec_mpt -spawn -np $nbr_parent ./boss.exe  >& log.interintra