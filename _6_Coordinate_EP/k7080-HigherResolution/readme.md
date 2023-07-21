### TODO

- geoJSON centroids for all buildings
- grid%id (module_surface_driver.F > inest) > module_sf_noahdrv.F > module_sf_bep_bem.F
- ~~add new variable into namelist.input: https://youtu.be/JVZlo8WyGfs?t=2254~~
git clone --recurse-submodule https://github.com/wrf-model/WRF.git
ln -sf ../../../WPS/met_em.d01*.*.
- Do you need to inform every IDF for the mapping-wrf-ep?
- Each hourly timestep, part of grid points from the innermost domain will call BEP1D/spawn_children
    1. hourly timestep and the first update in this location.
        a. communicate with ep for updating.
    2. otherwise
        a. (curix, curiy) > (waste)
- WRF global xlat, xlong (shape and transfer through MPI)
- mappings from WRF grids to IDF centroids
- WRF calling = 1 (get all the mappings, save the 3D-WRF-Mapping-EP variable into spawn_children)
- WRF calling = 1 (curXlat, curXlong) > call necessary > get corresponding response 
(for each timestep, IDF callback functions will and must be called exactly once.)
- Deploy on cheyenne.ucar.edu
    a. 24 hours HRRR
    b. 100 by 100 innermost domain
    c. (optional) parallel computing WRF with 4 * 4 = 16 processors.

### notes
1. currently, building waste heat is normalized by conditioned building footprint. And divided by three floors.
2. ending_steps for 24 hours simulation should be 23 * nbr_steps_hr, since we have extra MPI calling from curitime = 1 (which is not mod(nbr_steps_hr) == 0).