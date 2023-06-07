### Average different type of buildings in an urban class
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1470
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L2214
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L1552
https://github.com/wrf-model/WRF/blob/21c72141142fc6c8d203d2bf79f1990e45a0aef8/phys/module_sf_bep_bem.F#L5336
https://github.com/NCAR/noahmp/blob/3be0b2860dab167006a0b3c4822e234ca253c3df/drivers/wrf/module_sf_noahmpdrv.F#L3737

### TODO
1. The actual location of the domain index
2. WRF will start and end the MPI call. As long as the number of callings from WRF is less than the number of timesteps in IDF, it's OK.