program mpi_app
    use mpi
    implicit none

    call spawn_children()

contains

    subroutine spawn_children()
        implicit none
        include 'mpif.h'
        integer :: ierr, rank, num_procs, new_comm, parent_comm, child_idx,status(MPI_STATUS_SIZE)
        integer ::  calling = 0, num_children = 1
        real(kind=8) :: received_data(2), random_oat_c
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
        call MPI_Comm_spawn(command, MPI_ARGV_NULL, num_children, MPI_INFO_NULL, &
                0, parent_comm, new_comm, MPI_ERRCODES_IGNORE, ierr)
        print *, "Parent comm: ", parent_comm, " new comm: ", new_comm

        do while (.true.)
            do child_idx = 1, num_children
                call random_number(random_oat_c)
                random_oat_c = 12 + int(random_oat_c * 28)
                call MPI_Send(random_oat_c, 1, MPI_REAL8, child_idx-1, 0, new_comm, ierr)
                call MPI_Recv(received_data(child_idx), 1, MPI_REAL8, child_idx-1, MPI_ANY_TAG, new_comm, status, ierr)
            end do
            print *, "received_data", received_data
            if (status(MPI_TAG) == 886) then
                print *, "ending messsage 886 received, exiting the loop"
                exit
            end if
        end do

        call MPI_Barrier(new_comm, ierr)
        call MPI_Comm_free(new_comm, ierr)
        call MPI_Comm_free(parent_comm, ierr)
        call MPI_Finalize(ierr)

    end subroutine spawn_children

end program mpi_app
