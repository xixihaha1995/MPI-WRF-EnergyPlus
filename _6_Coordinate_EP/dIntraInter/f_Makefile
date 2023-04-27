CC = mpicc
FC = mpif90
CFLAGS = -Wall -Wextra
FFLAGS = -Wall -Wextra

all: boss.exe child.exe

boss.exe: boss.f90
	$(FC) $(FFLAGS) -o boss.exe boss.f90

child.exe: child.c
	$(CC) $(CFLAGS) -o child.exe child.c

run: boss.exe
	mpirun -n 2 ./boss.exe

clean:
	rm -f boss.exe child.exe
