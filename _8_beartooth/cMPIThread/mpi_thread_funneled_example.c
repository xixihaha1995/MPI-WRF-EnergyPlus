#include <stdio.h>
#include <mpi.h>
#include <unistd.h>
#include <pthread.h>

void* print_pid_tid(void* arg) {
    pid_t pid = getpid();
    pthread_t tid = pthread_self();
    printf("Process %d: Thread PID: %d, TID: %lu\n", *(int*)arg, pid, tid);
    return NULL;
}

int main(int argc, char** argv) {
    int rank, provided;
    
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    printf("Process %d: Provided level of thread support: %d\n", rank, provided);
    
    pthread_t thread;
    pthread_create(&thread, NULL, print_pid_tid, &rank);
    pthread_join(thread, NULL);
    
    MPI_Finalize();
    
    return 0;
}
