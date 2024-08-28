### citation

```bibtex
@misc{0b73665f1cb394ab7613a63764767420db0aab6a4c9343bf29ccdc0171d02d3a,
title = {{Integrating Urban Microclimate Prediction into Large Scale Building Energy Modeling ...}},
author = {Lichen Wu},
url = {https://dx.doi.org/10.13140/rg.2.2.36195.53284},
year = {2023},
note = {{Description: Unpublished}},
language = {{en}},
}
```

### introduction

This repo includes thee full software developing path for integrating [EnergyPlus](https://github.com/NREL/EnergyPlus) into [WRF](https://github.com/wrf-model/WRF).
The integration part is developed using Fortran(MPC_SendRecv) in WRF, and C API (MPI_Recv, MPI_Send) for EnergyPlus building energy model.

### set the ep shared file path:
1. #libenergyplusapi.so.*
2. `export LD_LIBRARY_PATH=/usr/local/EnergyPlus-23-1-0`

### for compile
1.add include directories

2.add link directories (shared libraries path)

3.add link liraries (shared libraries name)


