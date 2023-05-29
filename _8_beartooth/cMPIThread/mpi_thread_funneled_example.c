#include <stdio.h>
#include <mpi.h>
#include <unistd.h>
#include <pthread.h>

#define MAX_MSG_LEN 128

void* print_pid_tid(void* arg) {
    pid_t pid = getpid();
    pthread_t tid = pthread_self();
    printf("Process %d: Thread PID: %d, TID: %lu\n", *(int*)arg, pid, tid);
    return NULL;
}

int main(int argc, char** argv) {
    int rank, provided, size;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    //print arguments
    printf("argc: %d\n", argc);
    for (int i = 0; i < argc; i++) {
        printf("argv[%d]: %s\n", i, argv[i]);
    }
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(processor_name, &size);
    printf("Rank %d from comm %d at processor %s, size: %d\n", rank, MPI_COMM_WORLD, processor_name, size);

    printf("Rank %d: Provided level of thread support: %d\n", rank, provided);
    
    pthread_t thread;
    pthread_create(&thread, NULL, print_pid_tid, &rank);
    pthread_join(thread, NULL);
    
    MPI_Finalize();
    
    return 0;
}
