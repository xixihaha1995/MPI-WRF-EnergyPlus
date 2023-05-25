CC = mpicc
CFLAGS = -Wall -Wextra

all: parent.exe child.exe

parent.exe: parent.c
	$(CC) $(CFLAGS) -o parent.exe parent.c

child.exe: child.c
	$(CC) $(CFLAGS) -o child.exe child.c

run: parent.exe
	mpirun -np 2 ./parent.exe

clean:
	rm -f parent.exe child.exe
