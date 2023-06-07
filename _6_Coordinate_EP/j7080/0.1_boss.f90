program mpi_app
    integer :: time_idx, timesteps = 6 * 24 + 10, allix = 3, alliy =3, curix, curiy, curibui = 1, curitime
    real(kind=8) :: random_oat_c,mean_recv_waste_j

    do time_idx = 1, timesteps
        do curiy = 1, alliy
            do curix = 1, allix
                call random_number(random_oat_c)
                random_oat_c = 12 + int(random_oat_c*28)
                call spawn_children(curix,curiy,curibui,curitime,random_oat_c,mean_recv_waste_j)
                print * , "mean_recv_waste_j", mean_recv_waste_j
            end do
        end do
    end do

contains

    subroutine spawn_children(curix,curiy,curibui,curitime,random_oat_c,mean_recv_waste_j)
        implicit none
        include 'mpif.h'
        integer :: ierr, rank, num_procs, parent_comm, child_idx, status(MPI_STATUS_SIZE), curix, curiy, curibui, curitime
        integer, save :: new_comm,  saveix, saveiy, saveibui
        integer ::  calling = 0, num_children = 3, ending_steps = 6*20, ucm_tag = 0
        REAL(KIND=8), DIMENSION(:), ALLOCATABLE :: received_data
        real(kind=8) :: random_oat_c, mean_recv_waste_j
        logical :: initedMPI, spawned = .false., turnMPIon = .true.
        character(len=50) :: command
        ALLOCATE (received_data(num_children))

        if (calling == 0) then
            saveix = curix
            saveiy = curiy
            saveibui = curibui
        end if

        !if curix and curiy are not the same as saveix and saveiy, then return
        if (curix /= saveix .or. curiy /= saveiy .or. curibui /= saveibui) then
            !print *, "curix /= saveix .or. curiy /= saveiy .or. curibui /= saveibui, return"
            return
        end if

        calling = calling + 1
        print *, "calling spawn_children() counts:", calling, "curix", curix, "curiy", curiy, "curibui", curibui, "curitime", curitime


       

        if (turnMPIon .eqv. .false.) then
            !print *, "turnMPIon is false, no more MPI calls"
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
            !print *, "MPI_COMM_WORLD", MPI_COMM_WORLD, "num_procs", num_procs, "rank", rank

            call MPI_Comm_dup(MPI_COMM_WORLD, parent_comm, ierr)
            command = "./child.exe"
            call MPI_Comm_spawn(command, MPI_ARGV_NULL, num_children, MPI_INFO_NULL, &
                    0, parent_comm, new_comm, MPI_ERRCODES_IGNORE, ierr)
            !print *, "Parent comm: ", parent_comm, " new comm: ", new_comm
        end if

        if (calling > ending_steps - 1) then
            ucm_tag = 886
            turnMPIon = .false.
        else
            ucm_tag = 0
        end if

        do child_idx = 1, num_children
!            call random_number(random_oat_c)
!            random_oat_c = 12 + int(random_oat_c*28)
            !            print *, "new_comm:", new_comm
            !            new_comm = -2080374783
            call MPI_Sendrecv(random_oat_c, 1, MPI_REAL8, child_idx - 1, ucm_tag, &
                    received_data(child_idx), 1, MPI_REAL8, child_idx - 1, MPI_ANY_TAG, new_comm, status, ierr)
        end do
        mean_recv_waste_j = sum(received_data)/num_children
        !print *, "WRF (Parent(s)) received_data (waste heat J)", received_data, "mean_recv_waste_j", mean_recv_waste_j


        if (ucm_tag == 886) then
!            print *, "WRF (Parent(s)) ending messsage 886 sent, &
!                    &to reach collective barrier,(no more inter-communicator calls)&
!                    & only WRF global setting call free and MPI_Finalize()"
            call MPI_Barrier(new_comm, ierr)
            !            call MPI_Comm_free(new_comm, ierr)
            !            call MPI_Comm_free(parent_comm, ierr)
            !            call MPI_Finalize(ierr)
        end if
    end subroutine spawn_children

end program mpi_app
