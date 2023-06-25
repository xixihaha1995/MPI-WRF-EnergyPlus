program mpi_app
    integer :: time_idx, timesteps = 24 * 540, allix = 3, alliy =3, allbui = 2, curix, curiy, curibui, curitime = 1
    integer :: ierr
    real, dimension (3) :: random_weather ! oat_c, abs_hum_kgw_kga, pressure_pa
    real :: random_data
    real, dimension(13) :: wM2_12K
    real, dimension(18) :: wrfWaste
    real, dimension(4,10,18) :: wrfSurface
    real, dimension(12) :: tempValues
    real :: dt = 6.67, xlat = 41.30, xlong = -105.59


    do time_idx = 1, timesteps
    ! print *, "WRF time_idx", time_idx
        do curiy = 1, alliy
            do curix = 1, allix
                do curibui = 1, allbui
                    call random_number(random_data)
                    random_weather(1) = 12 + int(random_data*28)
                    random_weather(2) = 0.007612 + int(random_data*0.0001)
                    random_weather(3) = 101325 + int(random_data*1000)
                    call spawn_children(curix,curiy,curibui,dt,time_idx,xlat, xlong, random_weather,wM2_12K)
                    if (wM2_12K(1) < 0) then 
                        continue
                    end if
                    wrfWaste(1:7) = wM2_12K(1)
                    do i = 1, 3
                        wrfSurface(:,10, i) = wM2_12K(2+(i-1)*4:5+(i-1)*4)
                    end do
                    ! print *, 'wM2_12K', wM2_12K
                    ! print *, "wrfWaste(1:7)", wrfWaste(1:7)
                    ! print *, "wrfSurface(:,10,1:3)", wrfSurface(:,10,1:3)
                    
                end do
            end do
        end do
    end do

    print *, "WRF boss ended"


contains

 subroutine spawn_children(curix,curiy,curibui,dt,curitime,xlat, xlong,wrf_weather,wM2_12K)
      implicit none
      include 'mpif.h'
      integer :: ierr, rank, num_procs, parent_comm, child_idx, status(MPI_STATUS_SIZE), curix, curiy, curibui, curitime
      integer, save :: new_comm,  saveix, saveiy, saveitime = -1
      integer ::  calling = 0, ending_steps = (23 ) * 540, ucm_tag = 0
      integer, parameter ::  num_children = 1, performance_length = 14, weatherLength = 3, wrfNeedLen = 13
      real, dimension(num_children, performance_length) :: received_data
      REAL, DIMENSION(weatherLength) :: wrf_weather
      real :: dt, xlat, xlong
      logical :: initedMPI, spawned = .false., turnMPIon = .true.
      character(len=50) :: command
    !   output variables
      real, dimension(wrfNeedLen) :: wM2_12K



      !ix,iy,ibui,dt,itimestep,xlat,xlong,wrf_weather, wM2_12K

      if (calling == 0) then
            saveix = curix
            saveiy = curiy
            wM2_12K = 300
            wM2_12K(1) = 0
      end if

      !saveix, saveiy, first building height call, not the last step
      if (curix /= saveix .or. curiy /= saveiy .or. curitime == saveitime .or. turnMPIon .eqv. .false.) then
          return
      else 
        calling = calling + 1
        saveitime = curitime
        if (calling /= 1 .and. mod(calling,540) /= 0) then
            return
        end if
      end if

    !   print *, 'Within spawn_children curix', curix, 'curiy', curiy, 'curibui', curibui, 'dt',dt, 'curitime', curitime
    !   print *, 'Within spawn_children xlat', xlat, 'xlong', xlong, 'wM2_12K', wM2_12K
    !   print *, "Calling happening, calling", calling
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
    
      print *, "my calling", calling, "curitime", curitime, "saveitime", saveitime

      do child_idx = 1, num_children
          call MPI_Sendrecv(wrf_weather, weatherLength, MPI_REAL, child_idx - 1, ucm_tag, &
                  received_data(child_idx, :), performance_length,MPI_REAL, child_idx - 1, MPI_ANY_TAG, new_comm, status, ierr)
      end do
      wM2_12K(1) = sum(received_data(:, 2)) / num_children /sum (received_data(:, 1))
      ! for received_data(:, 3:14), 3:14 are the 12 surface temperatures, average them
      wM2_12K(2:13) = sum(received_data(:, 3:14), dim=1) / num_children
      print *, "WRF (Parent(s)) received_data (m2;w;12 surface[K])", received_data
      print *, "WRF (Parent(s)) wM2_12K", wM2_12K


      if (ucm_tag == 886) then
         print *, "WRF (Parent(s)) ending messsage 886 sent, &
                 &to reach collective barrier,MPI about to end, no more inter-communicator calls."
          call MPI_Barrier(new_comm, ierr)
          ! call MPI_Comm_free(new_comm, ierr)
          ! call MPI_Comm_free(parent_comm, ierr)
        !   call MPI_Finalize(ierr)
      end if
  end subroutine spawn_children
end program mpi_app
