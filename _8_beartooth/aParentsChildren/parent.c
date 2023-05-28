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
    int rank, size, nbr_child = 1;
    char* command = "/home/lwu4/fortran_experiments/_8_beartooth/aParentsChildren/child.exe";
    char msgstr[MAX_MSG_LEN];
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    MPI_Status status;
    MPI_Info info;
    MPI_Comm child_comm;

    MPI_Info_create(&info);
    MPI_Info_set(info, "host", "m199");
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(processor_name, &size);

    MPI_Comm_spawn(command, MPI_ARGV_NULL, nbr_child, info, 0, MPI_COMM_WORLD, &child_comm, MPI_ERRCODES_IGNORE);
 
    
    printf("Parent %d from comm %d at processor %s\n", rank, MPI_COMM_WORLD, processor_name);

}
