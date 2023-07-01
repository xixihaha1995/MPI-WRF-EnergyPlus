### Coordinate Large Scale IDFs with WRF

Both 22-2-0 23-1-0 should be able to be used on Cheyenne.
If it's slow, please correct IDF schedule pathes, and associated library `python_standard_lib` in the same path as `child.exe`.

My `~/.bashrc` setting
```
alias cdw='cd /glade/work/lichenwu/NWP'
alias cds='cd /glade/scratch/lichenwu'
alias cdf='cd /glade/work/lichenwu/fortran_experiments'
alias cdr='cd /glade/work/lichenwu/NWP/WRF/test/em_real'
export WRF_DIR='/glade/work/lichenwu/NWP/WRF'
export WPS_DIR='/glade/work/lichenwu/NWP/WPS'
export FOR_DIR='/glade/work/lichenwu/fortran_experiments'
export EM_REAL='/glade/work/lichenwu/NWP/WRF/test/em_real'
#export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/EnergyPlus-23-1-0:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/EnergyPlus-22-1-0:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/gcc_built_ep_23_1_0:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/gcc-built-up-ep-22-2-0:$LD_LIBRARY_PATH
export PATH=/glade/u/apps/ch/opt/ncarcompilers/0.5.0/intel/19.1.1:$PATH
export PATH=/glade/u/home/lichenwu/.local/bin:$PATH
```

Compile EnergyPlus-23.1.0 with GNU on cheyenne.ucar.edu
```
module load gnu/11.2.0
module load cmake/3.18.2
module load python/3.7.9
mkdir building-ep23-1-0
mkdir building-ep23-1-0/build
cd building-ep23-1-0
wget https://github.com/NREL/EnergyPlus/archive/refs/tags/v23.1.0.tar.gz
tar xzvf v23.1.0.tar.gz
cd build
cmake -DCMAKE_INSTALL_PREFIX=/glade/u/home/lichenwu/project/gcc-built-up-ep-23-1-0 ../EnergyPlus-23.1.0/
make -j 10
make install
# Add the following into ~/.bashrc
# export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/gcc-built-up-ep-22-2-0:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/glade/u/home/lichenwu/project/gcc_built_ep_23_1_0:$LD_LIBRARY_PATH
```

clone and modify the WRF source code
```
phys/module_physics_init.F
line 3363 - 3366
 !              IF (config_flags%use_wudapt_lcz.eq.1 .and. max_utype_urb2d.le.3.0) THEN  ! new LCZ
 !                CALL wrf_error_fatal &
 !                ('USING URBPARM_LCZ.TBL WITH OLD 3 URBAN CLASSES. SET USE_WUDAPT_LCZ=0')
 !              ENDIF

 ! spawn_children()
 #cp ~/project/NWP/WRF/phys/module_sf_bep_bem.F saved.cheyenne.sfbepbem.F
 ```


Compile WRF with GNU cheyenne.ucar.edu
```
module load gnu/11.2.0
./configure
34
1
./compile em_real -j 30 >& log.compile
```
Compile EnergyPlus API based customized program(child.exe)with GNU
```
#Pay attention to the FLAGS@Makefile
CFLAGS=-I/glade/u/home/lichenwu/project/building_ep23-1-0/EnergyPlus-23.1.0/src/
LDFLAGS=-L/glade/u/home/lichenwu/project/gcc_built_ep_23_1_0
LDLIBS = -lenergyplusapi

make
# copy customized child.exe and all the EnergyPlus input files into the WRF running folder
#cp child.exe ~/NWP/WRF/test/em_real
#cp -r ../../_6_Coordinate_EP/j7080/resources-23-1-0/ ~/project/NWP/WRF/test/em_real
 ```
Run the integrated program
```
cp nested24.namelist.wps ~/project/NWP/WPS/namelist.wps
cp nested24.namelist.input ~/project/NWP/WRF/test/em_real/namelist.input

cdw
cd WPS/
ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
./link_grib.csh ../DATA/fnl
./ungrib.exe
./geogrid.exe
./metgrid.exe
cd ../WRF/test/em_real/
ln -sf ../../../WPS/met_em.d0* .
./real.exe
qsub pbs.wrf.ep.csh
```


 ### Notes

 1. The major difference between HPC and personal computer is number of IDFs.
 2. Run small case on personal computer first.
 3. Try to manually modify the source code.
 4. Copy all the dependencies, *.exe, library, *.IDF, *.epw, *schedule.csv, into /WRF/test/em_real
 3. Module load gnu/11.2.0