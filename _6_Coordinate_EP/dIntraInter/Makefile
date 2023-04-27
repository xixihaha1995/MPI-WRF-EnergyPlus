CC = mpicc
CFLAGS = -Wall -Wextra

all: boss.exe child.exe

boss.exe: boss.c
	$(CC) $(CFLAGS) -o boss.exe boss.c

child.exe: child.c
	$(CC) $(CFLAGS) -o child.exe child.c

run: boss.exe
	mpirun -np 2 ./boss.exe

clean:
	rm -f boss.exe child.exe
