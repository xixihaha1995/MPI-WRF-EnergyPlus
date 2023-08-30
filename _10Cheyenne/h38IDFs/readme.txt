Building id = 1, lat = 41.31529750000000, lon = -105.58152500000001,is assigned to WRF#2, grid 74, lat = 41.31533050537109, lon = -105.58161926269531
Building id = 2, lat = 41.31328985009802, lon = -105.58458895073731,is assigned to WRF#2, grid 22, lat = 41.31347656250000, lon = -105.58409118652344
Building id = 3, lat = 41.31521200000000, lon = -105.57892600000000,is assigned to WRF#3, grid 51, lat = 41.31533050537109, lon = -105.57914733886719
Building id = 4, lat = 41.31471016569262, lon = -105.58097283264756,is assigned to WRF#3, grid 25, lat = 41.31440353393555, lon = -105.58038330078125
Building id = 5, lat = 41.31285600000000, lon = -105.58469850000000,is assigned to WRF#2, grid 22, lat = 41.31347656250000, lon = -105.58409118652344
Building id = 6, lat = 41.31263934779172, lon = -105.58478026072071,is assigned to WRF#2, grid 21, lat = 41.31347656250000, lon = -105.58532714843750
Building id = 7, lat = 41.31325170572097, lon = -105.58278955632146,is assigned to WRF#2, grid 23, lat = 41.31347656250000, lon = -105.58285522460938
Building id = 8, lat = 41.31544537887324, lon = -105.58496121830989,is assigned to WRF#2, grid 71, lat = 41.31533050537109, lon = -105.58532714843750
Building id = 9, lat = 41.31525970850574, lon = -105.58081190714407,is assigned to WRF#3, grid 50, lat = 41.31533050537109, lon = -105.58038330078125
Building id = 10, lat = 41.31292052915499, lon = -105.58363317559386,is assigned to WRF#2, grid 22, lat = 41.31347656250000, lon = -105.58409118652344

Comparision experiments
Form 1000m spatial resolution to 100m spatial resolution (6 hour simulation first)
1. *.csh, 
    a.For 1000m spatial resolution#PBS -l walltime=00:30:00, #PBS -l select=2:mpiprocs=36
    b.For 100m spatial resolution#PBS -l walltime=03:30:00,  #PBS -l select=2:mpiprocs=36
2. saved.module_sf_bep_bem.F,
    a.inner_dt = 6; running_hours = 6; num_children = 38
    b.inner_dt = 0.6; running_hours = 71; num_children = 38