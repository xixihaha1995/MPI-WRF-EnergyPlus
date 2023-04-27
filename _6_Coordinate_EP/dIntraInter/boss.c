#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#define MAX_MSG_LEN 128
void spawn_children(void);

int main(int argc, char** argv) {

    MPI_Init(&argc, &argv);

    spawn_children();
    MPI_Finalize();
    return 0;
}

void spawn_children(void) {
    int rank, size;
    char* command = "./child.exe";
    char msgstr[MAX_MSG_LEN];
    MPI_Status status;
    MPI_Comm child_comm;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);


    MPI_Comm_spawn(command, MPI_ARGV_NULL, 3, MPI_INFO_NULL, 0, MPI_COMM_WORLD, &child_comm, MPI_ERRCODES_IGNORE);
    MPI_Send("Hello", MAX_MSG_LEN, MPI_CHAR, 2, 0, child_comm);
    printf("Parent %d sent %s to %d of comm %d\n", rank, "Hello", 2, child_comm);
    if (rank == 1) {
        MPI_Recv(&msgstr, MAX_MSG_LEN, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, child_comm, &status);
        printf("Parent %d received %s from %d of comm %d\n", rank, msgstr, status.MPI_SOURCE, child_comm);
//        Intra from rank 0 to 1
        MPI_Recv(&msgstr, MAX_MSG_LEN, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        printf("Parent Intra %d received %s from %d of comm %d\n", rank, msgstr, status.MPI_SOURCE, MPI_COMM_WORLD);
    } else if (rank == 0) {
        MPI_Send("Rank 0 to 1", MAX_MSG_LEN, MPI_CHAR, 1, 0, MPI_COMM_WORLD);
    }
}
