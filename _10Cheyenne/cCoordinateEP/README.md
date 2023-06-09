### Coordinate Large Scale IDFs with WRF

Both 22-2-0 23-1-0 should be able to be used on Cheyenne.
If it's slow, please correct IDF schedule pathes, and associated library `python_standard_lib` in the same path as `child.exe`.

```
module load gnu/11.2.0
module load cmake/3.18.2
module load python/3.7.9
wget https://github.com/NREL/EnergyPlus/archive/refs/tags/v23.1.0.tar.gz
cmake -DCMAKE_INSTALL_PREFIX=/glade/u/home/lichenwu/project/gcc-built-up-ep-23-1-0 ../EnergyPlus-23.1.0/
make -j 10
make install
```

```
phys/module_physics_init.F
line 3363 - 3366
 !              IF (config_flags%use_wudapt_lcz.eq.1 .and. max_utype_urb2d.le.3.0) THEN  ! new LCZ
 !                CALL wrf_error_fatal &
 !                ('USING URBPARM_LCZ.TBL WITH OLD 3 URBAN CLASSES. SET USE_WUDAPT_LCZ=0')
 !              ENDIF

 ! spawn_children()
 ```

 ### Notes

 1. The major different between HPC and personal computer is number of IDFs.
 2. Run small case on personal computer first.
 3. Try to manually modify the source code.
 4. Copy all the dependencies, *.exe, library, *.IDF, *.epw, *schedule.csv, into /WRF/test/em_real
 3. Module load gnu/11.2.0