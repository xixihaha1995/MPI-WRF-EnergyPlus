### TODO

- geoJSON centroids for all buildings
- grid%id (module_surface_driver.F > inest) > module_sf_noahdrv.F > module_sf_bep_bem.F
- WRF global xlat, xlong
- mappings from WRF grids to IDF centroids
- WRF calling = 1 (get all the mappings, save the 3D-WRF-Mapping-EP variable into spawn_children)
- WRF calling = 1 (curXlat, curXlong) > call necessary > get corresponding response 
(for each timestep, IDF callback functions will and must be called exactly once.)