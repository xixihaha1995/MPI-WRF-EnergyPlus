program mpi_app
    integer :: time_idx, timesteps = 6 * 540, allix = 3, alliy =3, allbui = 2, curix, curiy, curibui, curitime = 1
    integer :: ierr
    real(kind=8), dimension (3) :: random_weather ! oat_c, abs_hum_kgw_kga, pressure_pa
    real(kind=8) :: mean_recv_waste_w_m2, random_data
    real :: dt = 6.67, xlat = 41.30, xlong = -105.59


    do time_idx = 1, timesteps
        do curiy = 1, alliy
            do curix = 1, allix
                do curibui = 1, allbui
                    call random_number(random_data)
                    random_weather(1) = 12 + int(random_data*28)
                    random_weather(2) = 0.007612 + int(random_data*0.0001)
                    random_weather(3) = 101325 + int(random_data*1000)
                    call spawn_children(curix,curiy,curibui,dt,time_idx,xlat, xlong, random_weather,mean_recv_waste_w_m2)
                    ! print * , "mean_recv_waste_w_m2", mean_recv_waste_w_m2
                end do
            end do
        end do
    end do

    print *, "WRF boss ended"


contains

 subroutine spawn_children(curix,curiy,curibui,dt,curitime,xlat, xlong,random_weather,mean_recv_waste_w_m2)
      implicit none
      include 'mpif.h'
      integer :: ierr, rank, num_procs, parent_comm, child_idx, status(MPI_STATUS_SIZE), curix, curiy, curibui, curitime
      integer, save :: new_comm,  saveix, saveiy, saveitime = -1
      integer ::  calling = 0, num_children = 1, ending_steps = (6 ) * 540, ucm_tag = 0
      REAL(KIND=8), DIMENSION(:), ALLOCATABLE :: received_data
      REAL(KIND=8), DIMENSION(3) :: random_weather
      real(kind=8) :: mean_recv_waste_w_m2
      real(kind=8) :: saved_waste_w_m2 = 0
      real :: dt, xlat, xlong
      logical :: initedMPI, spawned = .false., turnMPIon = .true., hourlyUpdate = .false.
      character(len=50) :: command
      ALLOCATE (received_data(num_children))

      !ix,iy,ibui,dt,itimestep,xlat,xlong,random_weather, mean_recv_waste_w_m2

      if (calling == 0) then
          saveix = curix
          saveiy = curiy
      end if

      !if curix and curiy are not the same as saveix and saveiy, then return
      if (curix /= saveix .or. curiy /= saveiy) then
          return
      end if
    
      if (curitime /= saveitime) then
            calling = calling + 1
            saveitime = curitime
            hourlyUpdate = .true.
        else
            hourlyUpdate = .false.
      end if
      
      ! print *, "calling spawn_children() counts:", calling, "curix", curix, "curiy", curiy
      ! print *, "curibui", curibui, "curitime", curitime
     
      !if calling is % 540, for 6.667s per step; 540 steps for one hour, then carry on, otherwise return
      if (mod(calling,540) /= 0 .or. hourlyUpdate .eqv. .true.) then
            ! Forward filling for any time steps, any building types
            mean_recv_waste_w_m2 = saved_waste_w_m2
            print *, "Forward filling curitime", curitime, "curibui", curibui
            return
      end if

      if (turnMPIon .eqv. .false.) then
          !print *, "turnMPIon is false, no more MPI calls"
          return
      end if
      print *, 'Within spawn_children curix', curix, 'curiy', curiy, 'curibui', curibui, 'dt',dt, 'curitime', curitime
      print *, 'Within spawn_children xlat', xlat, 'xlong', xlong
      print *, "Calling happening, calling", calling
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
          call MPI_Sendrecv(random_weather, 3, MPI_REAL8, child_idx - 1, ucm_tag, &
                  received_data(child_idx), 1, MPI_REAL8, child_idx - 1, MPI_ANY_TAG, new_comm, status, ierr)
      end do
      mean_recv_waste_w_m2 = sum(received_data)/num_children
      saved_waste_w_m2 = mean_recv_waste_w_m2
      !print *, "WRF (Parent(s)) received_data (waste heat J)", received_data, "mean_recv_waste_w_m2", mean_recv_waste_w_m2


      if (ucm_tag == 886) then
         print *, "WRF (Parent(s)) ending messsage 886 sent, &
                 &to reach collective barrier,MPI about to end, no more inter-communicator calls."
          call MPI_Barrier(new_comm, ierr)
          ! call MPI_Comm_free(new_comm, ierr)
          ! call MPI_Comm_free(parent_comm, ierr)
         !  call MPI_Finalize(ierr)
      end if
  end subroutine spawn_children
end program mpi_app
