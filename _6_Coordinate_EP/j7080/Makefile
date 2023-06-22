MPIF90 = mpif90
MPICC = mpicc

CFLAGS = -I/usr/local/EnergyPlus-23-1-0/include
LDFLAGS = -L/usr/local/EnergyPlus-23-1-0
LDLIBS = -lenergyplusapi

# Set LD_LIBRARY_PATH
export LD_LIBRARY_PATH := /usr/local/EnergyPlus-23-1-0:$(LD_LIBRARY_PATH)

FFLAGS =
CHILD = 0.1_child.c
BOSS = 0.1_boss.f90

MPI_APP = mpi_app
CHILD_EXE = child.exe

BOSS_OBJ = $(BOSS:.f90=.o)
CHILD_OBJ = $(CHILD:.c=.o)

.PHONY: all clean

all: $(MPI_APP) $(CHILD_EXE)

$(MPI_APP): $(BOSS_OBJ)
	$(MPIF90) $(FFLAGS) -o $@ $^

$(CHILD_EXE): $(CHILD_OBJ)
	$(MPICC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)

%.o: %.f90
	$(MPIF90) $(FFLAGS) -c -o $@ $<

%.o: %.c
	$(MPICC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(MPI_APP) $(CHILD_EXE) $(BOSS_OBJ) $(CHILD_OBJ)

run: all
	mpirun -np 1 ./$(MPI_APP)
