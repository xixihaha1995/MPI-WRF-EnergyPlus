#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char ** argv)
{
    int rank, size, ierr;
    int rand_num;

    ierr = MPI_Init(&argc, &argv);
    ierr = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    ierr = MPI_Comm_size(MPI_COMM_WORLD, &size);

    ierr = MPI_Bcast(&rand_num, 1, MPI_INT, 0, MPI_COMM_WORLD);
    printf("Worker %d received %d\n", rank, rand_num);
    MPI_Finalize();
    return 0;
}