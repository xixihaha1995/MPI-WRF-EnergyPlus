### Average different type of buildings in an urban class
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
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L3737

### Critical physical process of UCBEM

1. Urban climate
    a. Building emission.
    b. Building surface temperature.(TODO)
2. UBEM.
    a. Urban weather.
    b. shading
    c. Surrouding surface temperature (optional)

### TODO
1. EP: set temperature and humidity
2. WRF (finest domain) hourly communication with EP
3. WRF overrides surface temperature (averaged). [https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bem.F#L30]
4. WRF, EP, WEF+EP (T2m, Energy Consumption and Demand)
5. (7 days + 12 hours) simulation. WRF will start and end the MPI call. As long as the number of callings from WRF is less than the number of timesteps in IDF, it's OK.
6. WRF (send ix, iy to EnergyPlus); IDF models are tied with pairs of (ix, iy)

### EnergyPlus API
eplusout.rdd
Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Dewpoint Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Wetbulb Temperature,hourly; !- Zone Average [C]
Output:Variable,*,Site Outdoor Air Humidity Ratio,hourly; !- Zone Average [kgWater/kgDryAir]
Output:Variable,*,Site Outdoor Air Relative Humidity,hourly; !- Zone Average [%]
Output:Variable,*,Site Outdoor Air Barometric Pressure,hourly; !- Zone Average [Pa]
Output:Variable,*,Site Outdoor Air Enthalpy,hourly; !- Zone Average [J/kg]
Output:Variable,*,Site Outdoor Air Density,hourly; !- Zone Average [kg/m3]