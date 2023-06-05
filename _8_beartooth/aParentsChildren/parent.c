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
    int rank, world_size, nbr_child = 3, name_len;
    char* command = "./child.exe";
    char msgstr[MAX_MSG_LEN];
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    MPI_Status status;
    MPI_Comm child_comm;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    MPI_Get_processor_name(processor_name, &name_len);

   // MPI_Comm_spawn(command, MPI_ARGV_NULL, nbr_child, MPI_INFO_NULL, 0, MPI_COMM_WORLD, &child_comm, MPI_ERRCODES_IGNORE);

    printf("Parent: Rank %d from comm %d (size %d )at processor %s\n", rank, MPI_COMM_WORLD,world_size, processor_name);
    MPI_Finalize();
    return 0;
}
