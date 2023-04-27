program mpi_app
    use mpi
    implicit none

    integer :: ierr, num_procs, rank
    integer :: parent_comm, new_comm
    integer :: errorcodes(2)

    ! Initialize MPI
    call MPI_Init(ierr)

    ! Get the rank and number of processes in the parent communicator
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, num_procs, ierr)

    ! Spawn two child processes
    call spawn_children()

    ! Finalize MPI
    call MPI_Finalize(ierr)

contains

    subroutine spawn_children()
        use mpi
        implicit none
        integer :: ierr, new_comm
        integer, dimension(2) :: errorcodes
        character(len=50) :: command
        integer :: i

        ! Duplicate the parent communicator
        call MPI_Comm_dup(MPI_COMM_WORLD, parent_comm, ierr)
        ! Spawn two child processes
        do i = 1, 2
            command = "./child.exe"
            call MPI_Comm_spawn(command, MPI_ARGV_NULL, 1, MPI_INFO_NULL, &
                    0, MPI_COMM_WORLD, new_comm, errorcodes(i), ierr)
        end do

    end subroutine spawn_children

end program mpi_app
