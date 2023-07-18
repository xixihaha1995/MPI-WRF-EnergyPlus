### TODO

- geoJSON centroids for all buildings
- grid%id (module_surface_driver.F > inest) > module_sf_noahdrv.F > module_sf_bep_bem.F
- ~~add new variable into namelist.input: https://youtu.be/JVZlo8WyGfs?t=2254~~
git clone --recurse-submodule https://github.com/wrf-model/WRF.git
ln -sf ../../../WPS/met_em.d01*.*.
- Do you need to inform every IDF for the mapping-wrf-ep?
- WRF global xlat, xlong (shape and transfer through MPI)
- mappings from WRF grids to IDF centroids
- WRF calling = 1 (get all the mappings, save the 3D-WRF-Mapping-EP variable into spawn_children)
- WRF calling = 1 (curXlat, curXlong) > call necessary > get corresponding response 
(for each timestep, IDF callback functions will and must be called exactly once.)