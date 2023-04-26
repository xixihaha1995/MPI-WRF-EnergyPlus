
CC=gcc
FC=gfortran
#cflags, one is for include, the other is for shared library
#-fPIC means position independent code, which is needed for shared library (plugin)
CFLAGS=-I/usr/local/EnergyPlus-23-1-0/include -fPIC
# add path to find shared library
LDFLAGS=-L/usr/local/EnergyPlus-23-1-0 -L./
#shared library name
LDLIBS=-lenergyplusapi -lxxxhhhplugin

#customizable executable name
#other customizations can be done her
#1. fortrain source code name: c_ep_hello.f90
#2. fortran object file name: c_ep_hello.o
#3. shared library source code name: ephello.c
#4. shared library name: libxxxhhhplugin.so
#5. executable name: myprogram

all: myprogram

myprogram: c_ep_hello.o libxxxhhhplugin.so
	$(FC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

c_ep_hello.o: c_ep_hello.f90
	$(FC) -c $< -o $@

libxxxhhhplugin.so: ephello.c
	$(CC) $(CFLAGS) -shared -o $@ $<

clean:
	rm -f myprogram c_ep_hello.o libxxxhhhplugin.so
