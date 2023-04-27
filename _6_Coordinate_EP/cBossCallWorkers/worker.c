#include <stdio.h>
#include <mpi.h>


int main(int argc, char *argv[])
{
    int rank, size;
    float random_numbers[2], result;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

//    Worker to get jobs
    printf("Worker %d: Waiting for jobs\n", rank);
    MPI_Recv(&random_numbers, 2, MPI_REAL, 0, MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    result = random_numbers[0] + random_numbers[1];
    printf("Worker %d: %f + %f = %f\n", rank, random_numbers[0], random_numbers[1], result);
    MPI_Send(&result, 1, MPI_REAL, 0, 0, MPI_COMM_WORLD);

    MPI_Finalize();
    return 0;
}