#include <mpi.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#define MAX_MSG_LEN 128

int main(int argc, char** argv) {
    int rank, intrasize, intersize;
    char msgstr[MAX_MSG_LEN];
    MPI_Comm parent_comm;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_get_parent(&parent_comm);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &intersize);
    MPI_Comm_size(parent_comm, &intrasize);

    if (rank ==2)
    {
        MPI_Recv(&msgstr, MAX_MSG_LEN, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
        printf("Child %d received %s from %d of comm %d\n", rank, msgstr, status.MPI_SOURCE, parent_comm);
        MPI_Recv(&msgstr, MAX_MSG_LEN, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
        printf("Child %d received %s from %d of comm %d\n", rank, msgstr, status.MPI_SOURCE, parent_comm);
//        SEND TO then rank of 1 of parent_comm
        sprintf(msgstr, "I'm child %d.", rank);
        MPI_Send(&msgstr, strlen(msgstr) + 1, MPI_CHAR, 1, 0, parent_comm);
    }
    MPI_Finalize();
    return 0;
}
