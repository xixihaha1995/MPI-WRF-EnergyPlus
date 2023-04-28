# Compiler commands
MPIF90 = mpif90
MPICC = mpicc

# Compiler flags
FFLAGS =
CFLAGS =

# Source files
BOSS = boss.f90
CHILD = child.c

# Object files
BOSS_OBJ = $(BOSS:.f90=.o)
CHILD_OBJ = $(CHILD:.c=.o)

# Executables
MPI_APP = mpi_app
CHILD_EXE = child.exe

.PHONY: all clean

all: $(MPI_APP) $(CHILD_EXE)

$(MPI_APP): $(BOSS_OBJ)
	$(MPIF90) $(FFLAGS) -o $@ $^

$(CHILD_EXE): $(CHILD_OBJ)
	$(MPICC) $(CFLAGS) -o $@ $^

%.o: %.f90
	$(MPIF90) $(FFLAGS) -c -o $@ $<

%.o: %.c
	$(MPICC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(MPI_APP) $(CHILD_EXE) $(BOSS_OBJ) $(CHILD_OBJ)

run: all
	mpirun -np 2 ./$(MPI_APP)
