### Use Command to compile and run
```bash
mpif90 -o boss boss.c 
mpicc -o worker worker.c

mpirun -np 1 ./boss : -np 3 ./worker
```