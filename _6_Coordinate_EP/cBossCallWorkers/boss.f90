program boss
    use mpi
    implicit none

    integer(C_INT) :: ierr, i, j
    integer(C_INT) :: num_workers = 3
    real :: rand_number(2), cur_result

    call MPI_INIT(ierr)
    do i = 1, num_workers
        call c_worker()
    end do
    call MPI_COMM_SIZE(MPI_COMM_WORLD, num_workers, ierr)

    do i = 1, num_workers
        !generate two random numbers
        do j = 1, 2
            call random_number(rand_number(j))
        end do
        call MPI_SEND(rand_number, 2, MPI_REAL, i, 0, MPI_COMM_WORLD, ierr)
    end do
    ! wait for all workers to finish
    do i = 1, num_workers
        call MPI_RECV(cur_result, 1, MPI_REAL, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE, ierr)
        print *, "Worker ", i, " returned ", cur_result
    end do

    call MPI_FINALIZE(ierr)
end program boss