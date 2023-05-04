program mpi_app
    integer :: time_idx, timesteps = 6 * 24 + 10

    do time_idx = 1, timesteps
        call spawn_children()
    end do

contains

    subroutine spawn_children()
        implicit none
        include 'mpif.h'
        integer :: ierr, rank, num_procs, parent_comm, child_idx, status(MPI_STATUS_SIZE)
        integer, save :: new_comm
        integer ::  calling = 0, num_children = 3, ending_steps = 6*24, ucm_tag = 0
        REAL(KIND=8), DIMENSION(:), ALLOCATABLE :: received_data
        real(kind=8) :: random_oat_c
        logical :: initedMPI, spawned = .false., turnMPIon = .true.
        character(len=50) :: command
        ALLOCATE (received_data(num_children))

        calling = calling + 1
        print *, "calling spawn_children() counts:", calling

        if (turnMPIon .eqv. .false.) then
            print *, "turnMPIon is false, no more MPI calls"
            return
        end if

        if (spawned .eqv. .false.) then
            spawned = .true.
            call MPI_Initialized(initedMPI, ierr)
            if (.not. initedMPI) then
                print *, "MPI not initialized, initializing"
                call MPI_Init(ierr)
            end if

            call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
            call MPI_Comm_size(MPI_COMM_WORLD, num_procs, ierr)
            print *, "MPI_COMM_WORLD", MPI_COMM_WORLD, "num_procs", num_procs, "rank", rank

            call MPI_Comm_dup(MPI_COMM_WORLD, parent_comm, ierr)
            command = "./child.exe"
            call MPI_Comm_spawn(command, MPI_ARGV_NULL, num_children, MPI_INFO_NULL, &
                    0, parent_comm, new_comm, MPI_ERRCODES_IGNORE, ierr)
            print *, "Parent comm: ", parent_comm, " new comm: ", new_comm
        end if

        if (calling > ending_steps - 1) then
            ucm_tag = 886
            turnMPIon = .false.
        else
            ucm_tag = 0
        end if

        do child_idx = 1, num_children
            call random_number(random_oat_c)
            random_oat_c = 12 + int(random_oat_c*28)
            !            print *, "new_comm:", new_comm
            !            new_comm = -2080374783
            call MPI_Sendrecv(random_oat_c, 1, MPI_REAL8, child_idx - 1, ucm_tag, &
                    received_data(child_idx), 1, MPI_REAL8, child_idx - 1, MPI_ANY_TAG, new_comm, status, ierr)
        end do
        print *, "WRF (Parent(s)) received_data (waste heat J)", received_data

        if (ucm_tag == 886) then
            print *, "WRF (Parent(s)) ending messsage 886 sent, &
                    &to reach collective barrier,(no more inter-communicator calls)&
                    & only WRF global setting call free and MPI_Finalize()"
            call MPI_Barrier(new_comm, ierr)
            !            call MPI_Comm_free(new_comm, ierr)
            !            call MPI_Comm_free(parent_comm, ierr)
            !            call MPI_Finalize(ierr)
        end if
    end subroutine spawn_children

end program mpi_app
