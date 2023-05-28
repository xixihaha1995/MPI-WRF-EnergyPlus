# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=
export J="-j 30"
export DIR="/project/communitybem/Build_WRF/LIBRARIES"
export FFLAGS="-m64"
export LD_LIBRARY_PATH=$DIR/lib:$DIR/grib2/lib:$DIR/netcdf/lib:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/hdf5/serial:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
export CC="gcc"
export CXX="g++"
export FC="gfortran"
export FCFLAGS="-m64"
export F77="gfortran"
export JASPERLIB="$DIR/grib2/lib"
export JASPERINC="$DIR/grib2/include"
export LDFLAGS="-L$DIR/lib -L$DIR/grib2/lib -L$DIR/curl/lib -L$DIR/netcdf/lib"
export CPPFLAGS="-I$DIR/include -I$DIR/grib2/include -I$DIR/curl/include -I$DIR/netcdf/include"
export PATH=$DIR/mpich/bin:$PATH
export PATH="$DIR/netcdf/bin:$PATH"
export NETCDF="$DIR/netcdf"
#export NETCDF_classic=1
export LIBS="-lnetcdf -lhdf5_hl -lhdf5 -lz"
export WRF_DIR="/project/communitybem/NWP/WRF"
