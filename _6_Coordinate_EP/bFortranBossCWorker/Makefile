# MPI program makefile

# Compiler options
F90 = mpif90
CC = mpicc
CFLAGS =
LDFLAGS =

# Source files
BOSS_SRC = boss.f90
WORKER_SRC = worker.c

# Object files
BOSS_OBJ = boss.o
WORKER_OBJ = worker.o

all: boss worker

boss: $(BOSS_OBJ)
	$(F90) $(LDFLAGS) -o $@.out $^

worker: $(WORKER_OBJ)
	$(CC) $(LDFLAGS) -o $@.out $^

$(BOSS_OBJ): $(BOSS_SRC)
	$(F90) -c $< -o $@

$(WORKER_OBJ): $(WORKER_SRC)
	$(CC) $(CFLAGS) -c $< -o $@

run: boss worker
	mpirun -np 3 ./worker.out : -np 1 ./boss.out

clean:
	rm -f *.o *.out
