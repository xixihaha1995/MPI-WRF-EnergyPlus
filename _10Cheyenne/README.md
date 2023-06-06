### EnergyPlus

https://github.com/NREL/EnergyPlus/releases/download/v23.1.0/EnergyPlus-23.1.0-87ed9199d4-Linux-Ubuntu22.04-x86_64.run



### Cheyenne

https://fastx.ucar.edu:3300/session/

In the NCAR Cheyenne environment, the `HPE Message Passing Toolkit (MPT) MPI library that is loaded by defaut.
https://www.hpe.com/psnow/doc/a00074669en_us
https://arc.ucar.edu/knowledge_base/72581529


### Compilation

https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example.12385/
git clone --recurse-submodule https://github.com/wrf-model/WRF.git

```
phys/module_physics_init.F
line 3363 - 3366
 !              IF (config_flags%use_wudapt_lcz.eq.1 .and. max_utype_urb2d.le.3.0) THEN  ! new LCZ
 !                CALL wrf_error_fatal &
 !                ('USING URBPARM_LCZ.TBL WITH OLD 3 URBAN CLASSES. SET USE_WUDAPT_LCZ=0')
 !              ENDIF
 ```

cd WRF
./configure (option 15 and 1)
./compile em_real -j 4 >& log.compile


wget "https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz"
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/cglc_modis_lcz_global.tar.gz
ln -sf GEOGRID.TBL.ARW_LCZ GEOGRID.TBL
ln -sf  GEOGRID.TBL.ARW_LCZ GEOGRID.TBL
wget "https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_06_00.grib2"
ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
./link_grib.csh ../DATA/matthew/fnl



