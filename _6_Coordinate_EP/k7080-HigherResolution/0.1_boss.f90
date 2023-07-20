program mpi_app
    integer :: time_idx, timesteps = 24 * 540, allix = 3, alliy =3, allbui = 2, curix, curiy, curibui, curitime = 1
    integer :: ierr
    integer, parameter :: its = 1, ite = 15, ims = 1, ime = 15, jms = 1, jme = 15
    real, dimension (3) :: random_weather ! oat_c, abs_hum_kgw_kga, pressure_pa
    real :: random_data
    real, dimension(13) :: wM2_12K
    real, dimension(18) :: wrfWaste
    real, dimension(4,10,18) :: wrfSurface
    real, dimension(12) :: tempValues
    real :: dt = 6.67, xlat = 41.30, xlong = -105.59
    real, dimension(its:ite, its:ite) :: xlatall, xlongall
    logical :: replaced

    xlatall = 41.30
    xlongall = -105.59


    do time_idx = 1, timesteps
    ! print *, "WRF time_idx", time_idx
        do curiy = 1, alliy
            do curix = 1, allix
                do curibui = 1, allbui
                    call random_number(random_data)
                    random_weather(1) = 12 + int(random_data*28)
                    random_weather(2) = 0.007612 + int(random_data*0.0001)
                    random_weather(3) = 101325 + int(random_data*1000)
                    call spawn_children(curix,curiy,curibui,dt,time_idx,its, &
                    ite,ims,ime,jms,jme,xlatall, xlongall, xlat, xlong, random_weather, replaced, wM2_12K)
                    if (replaced) then 
                        wrfWaste(1:7) = wM2_12K(1)
                        ! do i = 1, 3
                        !     wrfSurface(:,10, i) = wM2_12K(2+(i-1)*4:5+(i-1)*4)
                        ! end do
                    else
                        print *, 'offline; one way coupling from WRF -> EP'
                    end if
                end do
            end do
        end do
    end do

    print *, "WRF boss ended"


contains

subroutine spawn_children(curix,curiy,curibui,dt,curitime,&
    its, ite, ims,ime,jms,jme,xlatall, xlongall, xlat, xlong,wrf_weather,replaced,wM2_12K)
    implicit none
    include 'mpif.h'
    integer, parameter ::  nbr_steps_hr = 540
    integer :: ierr, rank, num_procs, parent_comm, child_idx, status(MPI_STATUS_SIZE), curix, curiy, curibui, curitime
    integer, save :: new_comm
    ! ending_steps for 24 hours simulation should be 23 * nbr_steps_hr, 
    ! since we have extra MPI calling from curitime = 1 (which is not mod(nbr_steps_hr) == 0)).
    integer ::  ending_steps = (5 ) * nbr_steps_hr, ucm_tag = 0
    integer, parameter ::  num_children = 3, performance_length = 2, weatherLength = 3, wrfNeedLen = 1
    real, dimension(num_children, performance_length) :: received_data
    REAL, DIMENSION(weatherLength) :: wrf_weather
    real :: dt, xlat, xlong
    logical :: initedMPI, spawned = .false., turnMPIon = .true., replaced
    character(len=50) :: command
!   output variables
    real, dimension(wrfNeedLen) :: wM2_12K
    integer :: ims, ime, jms, jme, its, ite
    REAL, DIMENSION(ims:ime, jms:jme), &
    INTENT(IN)  ::                           xlatall, xlongall
    REAL, DIMENSION(its:ite, its:ite, 1:wrfNeedLen) :: saved_wM2_12k
    integer :: saveitime(its:ite, its:ite)
    REAL, DIMENSION(:), ALLOCATABLE :: xlatall1d, xlongall1d
    INTEGER, DIMENSION(:), ALLOCATABLE :: mapping_wrf_ep
    INTEGER, DIMENSION(num_children) :: one_grid_mapping
    INTEGER :: latlongall_length, mapping_length
    integer :: i, j, k, map_left_idx, map_right_idx

    !ix,iy,ibui,dt,itimestep,xlat,xlong,wrf_weather, wM2_12K

    if (spawned .eqv. .false.) then
        spawned = .true.
        wM2_12K = 300
        wM2_12K(1) = 0
        saveitime = -1 
        print *, "saveitime", saveitime
        latlongall_length = (ite - its + 1)*(ite - its + 1)
        mapping_length = latlongall_length * num_children
        allocate(xlatall1d(latlongall_length))
        allocate(xlongall1d(latlongall_length))
        allocate(mapping_wrf_ep(mapping_length))
        
        !flatten the 2d arrays
        k = 1
        do i = its, ite
        do j = its, ite
            xlatall1d(k) = xlatall(i, j)
            xlongall1d(k) = xlongall(i, j)
            k = k + 1
        end do
        end do
        print *, "curitime", curitime
        print *, "xlatall(curix, curiy)", xlatall(curix, curiy), "xlongall(curix, curiy)", xlongall(curix, curiy)
        print *, "xlongall1d", xlongall1d
        print *, "xlatall1d", xlatall1d

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

        do child_idx = 1, num_children
        call MPI_Send(xlatall1d, latlongall_length, MPI_REAL, child_idx-1, 0, new_comm, ierr)
        call MPI_Send(xlongall1d, latlongall_length, MPI_REAL, child_idx-1, 0, new_comm, ierr)
        ! !Sent lat, long info to EnergyPlus, then a searching algo will be done to find the closest lat, long for 
        ! !each building IDF centroid.
        call MPI_Recv(mapping_wrf_ep, mapping_length, MPI_INTEGER, child_idx-1, 0, new_comm, status, ierr)
        end do

        print *, "mapping_wrf_ep", mapping_wrf_ep

    end if

    map_right_idx = ((curix - 1) * (ite - its + 1) + curiy) * num_children
    map_left_idx = map_right_idx - num_children + 1
    one_grid_mapping = mapping_wrf_ep(map_left_idx:map_right_idx)
    print *, "WRF grid index", ((curix - 1) * (ite - its + 1) + curiy),"corresponding IDF indices", one_grid_mapping

    if (.not. any(one_grid_mapping .gt. 0)) then
        replaced = .false.
        return
    else
        replaced = .true.
    end if

    if (turnMPIon .eqv. .false.) then
        !print *, "turnMPIon is false, no more MPI calls"
            return
    end if

    !hourly timestep
    print *, "curitime", curitime, "mod(curitime, nbr_steps_hr) /= 0?", mod(curitime, nbr_steps_hr) /= 0
    print *, "curitime /= 1?", curitime /= 1
    if (curitime == saveitime(curix, curiy) .or. mod(curitime, nbr_steps_hr) /= 0 .and. curitime /= 1) then
        ! to communicate with EnergyPlus for updating
        wM2_12K = saved_wM2_12k(curix, curiy, :)
        return
    end if

    saveitime(curix, curiy) = curitime

    if (curitime > ending_steps - 1) then
        ucm_tag = 886
        turnMPIon = .false.
        print *, "WRF (Parent(s)) ending messsage 886 sent, &
        &to reach collective barrier,MPI about to end, no more inter-communicator calls."
        call MPI_Barrier(new_comm, ierr)
        ! call MPI_Comm_free(new_comm, ierr)
        ! call MPI_Comm_free(parent_comm, ierr)
        !call MPI_Finalize(ierr)
    else
        ucm_tag = 0
    end if

    do child_idx = 1, num_children
        if (one_grid_mapping(child_idx) .gt. 0) then
        call MPI_Sendrecv(wrf_weather, weatherLength, MPI_REAL, child_idx - 1, ucm_tag, &
                received_data(child_idx, :), performance_length,MPI_REAL, child_idx - 1, MPI_ANY_TAG, new_comm, status, ierr)
        end if
    end do
    wM2_12K(1) = sum(received_data(:, 2)) / num_children /sum (received_data(:, 1))
    ! for received_data(:, 3:14), 3:14 are the 12 surface temperatures, average them
    !wM2_12K(2:13) = sum(received_data(:, 3:14), dim=1) / num_children
    print *, "WRF (Parent(s)) received_data (m2;w;12 surface[K])", received_data
    print *, "WRF (Parent(s)) wM2_12K", wM2_12K

end subroutine spawn_children
end program mpi_app
