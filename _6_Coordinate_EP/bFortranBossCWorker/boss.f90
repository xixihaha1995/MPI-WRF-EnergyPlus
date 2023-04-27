program boss
    use mpi
    implicit none
    integer :: rank, size, ierr
    integer :: rand_num

    call MPI_INIT(ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierr)
    call MPI_COMM_SIZE(MPI_COMM_WORLD, size, ierr)

    rand_num = randint()
    call MPI_BCAST(rand_num, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)

    write(*,*) 'Boss rank: ', rank, ' of ', size, ' with random number: ', rand_num

    call MPI_FINALIZE(ierr)

contains
    function randint() result(r)
        real :: r
        call random_seed()
        call random_number(r)
        r = r * 100
    end function randint

end program boss