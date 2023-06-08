### Coordinate Large Scale IDFs with WRF

```
module load gnu/11.2.0
module load cmake/3.18.2
module load python/3.7.9
wget https://github.com/NREL/EnergyPlus/archive/refs/tags/v22.2.0.tar.gz
cmake -DCMAKE_INSTALL_PREFIX=/glade/u/home/lichenwu/project/gcc-built-up-ep-22-2-0 ../EnergyPlus-22.2.0/
make -j 10
make install
```
