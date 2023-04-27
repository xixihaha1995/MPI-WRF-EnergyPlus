program main
    use iso_c_binding, only: c_int, c_funptr, c_null_ptr, c_funloc

    implicit none

    ! Declare the C function pointer
    type(c_funptr) :: myFunction_ptr

    ! Declare the global variable
    type(c_int), bind(C) :: numCalls

    ! Load the C function pointer
    myFunction_ptr = c_funloc("myFunction")

    ! Call myFunction through the C function pointer
    call c_f_procpointer(myFunction_ptr, numCalls)

    stop
end program main
