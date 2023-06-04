### WRF Related Notes
ln -sf  GEOGRID.TBL.ARW_LCZ GEOGRID.TBL
https://console.cloud.google.com/marketplace/product/noaa-public/hrrr?project=python-232920&pli=1
https://www.nco.ncep.noaa.gov/pmb/products/hrrr/
gsutil -m cp \
  "gs://high-resolution-rapid-refresh/hrrr.20230501/conus/hrrr.t00z.wrfprsf00.grib2" \
  .
ncdump -h geo_em.d01.nc
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/cglc_modis_lcz_global.tar.gz

wget "https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_06_00.grib2"
ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
wget "https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz"
ln -sf ../../../WPS/met_em.d01.2023-05-01_0* .

ncl util/plotgrids_new.ncl 

```
phys/module_physics_init.F
line 3363 - 3366
 !              IF (config_flags%use_wudapt_lcz.eq.1 .and. max_utype_urb2d.le.3.0) THEN  ! new LCZ
 !                CALL wrf_error_fatal &
 !                ('USING URBPARM_LCZ.TBL WITH OLD 3 URBAN CLASSES. SET USE_WUDAPT_LCZ=0')
 !              ENDIF
 ```
 
### ARCC
- https://arccwiki.atlassian.net/wiki/spaces/DOCUMENTAT/pages/3178497/Lmod+-+Software
- slurm introduction 1, 2
- module load mpich/3.0.4
- module load gcc/v12.2.0

checking for slurm/pmi.h... yes
checking for PMI_Init in -lpmi... no
configure: error: could not find the slurm libpmi.  Configure aborted

* WRF software installation request