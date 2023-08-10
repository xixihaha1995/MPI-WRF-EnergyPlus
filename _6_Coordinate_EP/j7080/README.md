### WRF domain design
Our "rule" is that each domain should be at least 100x100 (e_we and e_sn values). Take a look at this page for best practice suggestions on setting up your domain.

https://www.thoughtco.com/degree-of-latitude-and-longitude-distance-4070616#:~:text=A%20degree%20of%20longitude%20is,53%20miles%20(85%20kilometers).
https://forum.mmm.ucar.edu/threads/design-coarse-domain.10586/post-22296
https://forum.mmm.ucar.edu/threads/domain-design-the-ratio-among-domain-resolutions.329/post-913
https://www2.mmm.ucar.edu/wrf/users/namelist_best_prac_wps.html


HRRR 3km > 500m > 100m

```
ln -sf ungrib/Variable_Tables/Vtable.HRRR Vtable
./link_grib.csh ../DATA/HRRR07022022/

ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
./link_grib.csh ../DATA/fnl
```

#### 100m Spatial resolution 

GIS4WRF
https://gis4wrf.github.io/

#### HRRR 3km hourly
https://console.cloud.google.com/storage/browser/high-resolution-rapid-refresh/hrrr.20220702/conus?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false

https://console.cloud.google.com/marketplace/product/noaa-public/hrrr?project=python-232920&pli=1
https://www.nco.ncep.noaa.gov/pmb/products/hrrr/

Vtable:
‘prs’ pressure-level data should be used: https://github.com/blaylockbk/Ute_WRF/blob/5ccef028807f9fcf621ecfe3b1adc4616b27b211/modificaions/Vtable.HRRR.bkb#L49

```
gsutil -m cp \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t00z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t01z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t02z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t03z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t04z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t05z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t06z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t07z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t08z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t09z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t10z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t11z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t12z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t13z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t14z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t15z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t16z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t17z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t18z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t19z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t20z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t21z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t22z.wrfprsf00.grib2" \
  "gs://high-resolution-rapid-refresh/hrrr.20220702/conus/hrrr.t23z.wrfprsf00.grib2" \
  .
```

#### WRF-IDF mapping

1. geoJSON > centroid 
2. WRF iterates the innermost domain grids (send domain lat and long, urban weather).
3. IDF iterates through all buildings
  Within 2^0.5 * 50 meters, then the building will be bond with the current grid.

```c
#include <stdio.h>
#include <math.h>

double haversine(double lat1, double lon1, double lat2, double lon2) {
    double R = 6371;  // Earth's radius in kilometers

    // Convert latitude and longitude to radians
    double lat1_rad = lat1 * M_PI / 180;
    double lon1_rad = lon1 * M_PI / 180;
    double lat2_rad = lat2 * M_PI / 180;
    double lon2_rad = lon2 * M_PI / 180;

    // Calculate differences between coordinates
    double dlat = lat2_rad - lat1_rad;
    double dlon = lon2_rad - lon1_rad;

    // Apply Haversine formula
    double a = pow(sin(dlat / 2), 2) + cos(lat1_rad) * cos(lat2_rad) * pow(sin(dlon / 2), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double distance = R * c;

    return distance;
}

int main() {
    double lat1 = 41.313;
    double lon1 = -105.581;
    double lat2 = 41.213;
    double lon2 = -105.523;

    double distance = haversine(lat1, lon1, lat2, lon2);
    printf("Distance between the coordinates: %f kilometers\n", distance);

    return 0;
}
```

### General workflow

ln -sf ../../../WPS/met_em.d01.2016-10* .

### Critical physical process of UCBEM

1. Urban climate
    a. Building emission.
    b. Building surface temperature.(TODO)
2. UBEM.
    a. Urban weather.
    b. shading
    c. Surrouding surface temperature (optional)

### EnergyPlus API vs WRF API

```IDF
Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Dewpoint Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Wetbulb Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Humidity Ratio,hourly; !- Zone Average [kgWater/kgDryAir]
Output:Variable,*,Site Outdoor Air Relative Humidity,hourly; !- Zone Average [%]
Output:Variable,*,Site Outdoor Air Barometric Pressure,hourly; !- Zone Average [Pa]
Output:Variable,*,Site Outdoor Air Enthalpy,hourly; !- Zone Average [J/kg]
Output:Variable,*,Site Outdoor Air Density,hourly; !- Zone Average [kg/m3]

ConvergenceLimits,
  0,                       !- Minimum System Timestep {minutes}
  25;                      !- Maximum HVAC Iterations
```
```fortran
real tout(nzcanm)		!external temperature [K]
real humout(nzcanm)		!absolute humidity [Kgwater/Kgair]
real press(nzcanm)		!external air pressure [Pa]
```
### Building Surface Temperatures, and Pumped Waste Heat Usage
From surface temperature [K], waste heat [W] > tvb_u (Vertical surfaces, B (explicit) term) > vtb > b_t (Explicit component for the temperature)
b_t_bep > RTHBLTEN (Theta tendency due to PBL parameterization (m/s^2)) > t_tendf
t_tendf > t_tend > tendency for advecting temperatures for next timestep.

https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L184
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L179
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1726
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1727
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1749
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L4192
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L2849
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L3078
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L3099
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L118
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_noahdrv.F#L117
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_surface_driver.F#L2887
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_surface_driver.F#L292
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part1.F#L852
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part1.F#L1148
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_pbl_driver.F#L1222
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_bl_ysu.F#L295
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_bl_ysu.F#L1263
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_bl_ysu.F#L1283
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_bl_ysu.F#L313
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_bl_ysu.F#L19
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_pbl_driver.F#L1200
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_pbl_driver.F#L15
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part1.F#L1129
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part2.F#L795
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_physics_addtendc.F#L259
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_physics_addtendc.F#L2326
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_physics_addtendc.F#L259
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_physics_addtendc.F#L28
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part2.F#L793
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_first_rk_step_part2.F#L17
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/solve_em.F#L963
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_em.F#L1078
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/solve_em.F#L962
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/solve_em.F#L877
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_em.F#L625
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/dyn_em/module_advect_em.F#L3029

### Other BEM Surface Temperature Usage

From surface temperature [K], to ground/snow heat flux [W/m2]
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1470
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1620
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1726
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1773
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1816
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L2835
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L4192
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L2214
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1552
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L5336
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L222
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L3737

https://github.com/AmirAAliabadi/VCWGv1.4.5/blob/715ddf5558518d6d8e2b52e06c066d930178742a/UWG/BuildingColumnModel.py#L233
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L222
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L3737


### Detailed Design

1. How to get the actual location (especially longitude)?
Done. The `xlat` and `xlong` are already passed from `surface_driver` all the way to `subroutine BEP_BEM()`.
2. The following variables should also be backtracked: 
The spatial resolution? The temporal resolution?
3. The following illustrates `how the BEM module is initialized and computed`. For example, how `Thermal conductivity of roof [ J m{-1} s{-1} K{-1} ]` is defined and used?
a. 
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/run/URBPARM_LCZ.TBL#L262
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/run/URBPARM_LCZ.TBL#L426
b. https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L5139
c. https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L2033
d. https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1726
f. https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L729
g. https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L949

### Software Implementation TODO
1. ✅EP: set temperature and humidity
2. ✅`hourly communication with EP (WRF and UP hit barrier, WRF Finalize, UP Finalize, Then UP exit)
3. ✅Both 22-2-0 and 23-1-0 EnergyPlus should work on Cheyenne. Please make sure IDF schedule, and system pathes well configured.
4. ✅WRF (finest domain): (send ix, iy to EnergyPlus); 
5. WRF overrides surface temperature (averaged). [https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L30]
6. IDF models are tied with pairs of (ix, iy)

### Preliminary Study Report

We want to evaluate the impact of coupling methods on building energy consumption.
The followings are potential tuning options:
-1. fix the finest domain calling logics, calling frequencies 
  a. EnergyPlus is fixed at hourly simulation.
  b. As long as the finest domain within WRF, calls the EP module hourly (such as 6.67s * 540 = 3600s = 1 hr)
0. Waste heat and surface temperatures, units conversion.
The direct outputs from `subroutine BEM()` is `sflev1D sensible heat flux due to a.c. system [W]` 
or `hsout sensible heat emitted outside the floor[W]`, which is calculated from `Air conditioned floor area[m2]`, where Af = bw * bl, both are from the `URBPARM_LCZ.tbl`
But they also do nomalization at: https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L3028
The kick-start design of waste heat exchange:
Within one urban class grid, no matter how much its resolution are 10 km, or 100m, the actual total waste heat will be normalized first, then converted to WRF virtual urban grid footprint.

0.1. Get the averaged building surface temperature (shading or sunlit?)
Answer: 
One urban class > multiple actual buildings > virtual LCZ building (LCZ_1, AF = 12 * 12 = 144 m2)
Averaged heat performance (W/m2) * virtual building footprint (144 m2) = W (normalized waste heat in urban class)

Overall, the novelty of this study:
a. Compared with WRF, more detailed BEM.
b. Compared with VCWG+EP, real-time real-large urban climate model will be embedded with Urban Building Energy Model.
The real question is whether the current implementation a good urban climate model for large-community-scale BEM or not.
0.2 Dummy cases for preliminary case study: 
one urban class + one building (normalized waste heat, surface temperature)
// the above should be enough to see the coupling method impacts
0.3. The visualization of calculated temperatures. Pretty much, I need to pinpoint the urban temperature
0.4. Vertial resolution
0.5. Horizontal resolution