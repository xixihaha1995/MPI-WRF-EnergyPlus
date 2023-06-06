
CC=mpicc
CFLAGS=-I/glade/u/home/lichenwu/project/EnergyPlus-23-1-0/include
LDFLAGS=-L/glade/u/home/lichenwu/project/EnergyPlus-23-1-0
LDLIBS=-lenergyplusapi

test: _test1.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o test _test1.c $(LDLIBS)

clean:
	rm -f test
