program mpi_app
    use mpi
    implicit none

    call spawn_children()
    call spawn_children()
    call spawn_children()
    call spawn_children()


contains

    subroutine spawn_children()
        implicit none
        include 'mpif.h'
        integer :: ierr, rank, num_procs, new_comm, parent_comm, calling = 0
        logical :: inited
        character(len=50) :: command
        !define one global variable countCalling
        print *, "calling", calling
        if (calling > 0) then
            return
        end if
        calling = calling + 1

        call MPI_Initialized(inited, ierr)
        if (.not. inited) then
            call MPI_Init(ierr)
        end if
        call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
        call MPI_Comm_size(MPI_COMM_WORLD, num_procs, ierr)
        print *, "MPI_COMM_WORLD", MPI_COMM_WORLD, "num_procs", num_procs, "rank", rank

        call MPI_Comm_dup(MPI_COMM_WORLD, parent_comm, ierr)
        command = "./child.exe"
        call MPI_Comm_spawn(command, MPI_ARGV_NULL, 3, MPI_INFO_NULL, &
                0, parent_comm, new_comm, MPI_ERRCODES_IGNORE, ierr)
        print *, "Parent comm: ", parent_comm, " new comm: ", new_comm
        call MPI_Send(666666, 1, MPI_INTEGER, 2, 0, new_comm, ierr)

    end subroutine spawn_children

end program mpi_app
