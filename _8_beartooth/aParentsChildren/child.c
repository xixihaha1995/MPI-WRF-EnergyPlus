#include <mpi.h>
#include <stdio.h>
#include <unistd.h>
#define MPI_MAX_PROCESSOR_NAME 128

int main(int argc, char** argv) {
    int rank, size, msg, namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    MPI_Comm parent_comm;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_get_parent(&parent_comm);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(processor_name, &namelen);

    printf("Child/parent %d/%d: rank=%d, size=%d, name=%s\n", MPI_COMM_WORLD, parent_comm, rank, size, processor_name);
    return 0;
}
