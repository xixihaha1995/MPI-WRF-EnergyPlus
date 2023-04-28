
# fortran_plugin_Makefile

FC = gfortran
FFLAGS = -g -Wall
LDFLAGS = -L./ -lplugin

all: test

test: python_hello.f90
	$(FC) $(FFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f test *.h *.c *.so *.o
