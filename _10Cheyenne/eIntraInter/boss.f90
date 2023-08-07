program mpi_example
    use mpi
    implicit none
    integer ::  ierr
    call MPI_Init(ierr)

    call spawn_children()
    call MPI_Finalize(ierr)
end program mpi_example

subroutine spawn_children()
    use mpi
    implicit none
    integer, parameter :: MPI_MAX_CHAR = 128
    integer :: ierr, child_comm, rank, size, status(MPI_STATUS_SIZE), msglen
    character(len=*), parameter :: command = "./child.exe"
    character(len=MPI_MAX_CHAR) :: message

    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)
    call MPI_Comm_spawn(command, MPI_ARGV_NULL, 3, MPI_INFO_NULL, 0, MPI_COMM_WORLD, &
            child_comm, MPI_ERRCODES_IGNORE, ierr)
    call MPI_Send("Hello", MPI_MAX_CHAR, MPI_CHAR, 2, 0, child_comm, ierr)
    if (rank == 1) then
        call MPI_Recv(message, MPI_MAX_CHAR, MPI_CHAR, 2, 0, child_comm, status, ierr)
        call MPI_Get_count(status, MPI_CHAR, msglen, ierr)
        print *, "length of message: ", msglen, " message: ", message(1:msglen)
    end if
end subroutine spawn_children