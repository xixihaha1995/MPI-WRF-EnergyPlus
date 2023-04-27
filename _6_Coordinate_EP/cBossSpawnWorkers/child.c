#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    int rank, size;
    MPI_Comm parent_comm;

    MPI_Init(&argc, &argv);
    MPI_Comm_get_parent(&parent_comm);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    printf("Child process %d/%d: rank=%d, size=%d\n", getpid(), MPI_COMM_WORLD, rank, size);

    MPI_Finalize();
    return 0;
}
