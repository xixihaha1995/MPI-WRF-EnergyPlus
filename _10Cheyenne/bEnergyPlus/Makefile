CC=mpicc
CFLAGS=-I/glade/u/home/lichenwu/project/building_ep23-1-0/EnergyPlus-23.1.0/src/
LDFLAGS=-L/glade/u/home/lichenwu/project/gcc_built_ep_23_1_0
LDLIBS=-lenergyplusapi

# export LD_LIBRARY_PATH := /glade/u/home/lichenwu/project/gcc_built_ep_23_1_0:$(LD_LIBRARY_PATH)

test: _test1.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o test _test1.c $(LDLIBS)

clean:
	rm -f test
