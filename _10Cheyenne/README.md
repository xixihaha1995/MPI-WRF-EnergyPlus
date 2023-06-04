### Cheyenne

https://fastx.ucar.edu:3300/session/

### Compilation

https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example.12385/
git clone --recurse-submodule https://github.com/wrf-model/WRF.git
cd WRF
./configure (option 15 and 1)
./compile em_real -j 4 >& log.compile


wget "https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz"
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/cglc_modis_lcz_global.tar.gz
wget "https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_06_00.grib2"
ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
./link_grib.csh ../DATA/matthew/fnl



