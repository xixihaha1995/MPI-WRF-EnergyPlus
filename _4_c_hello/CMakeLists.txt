
cmake_minimum_required(VERSION 3.0)

project(myprogram)

# Set the Fortran compiler
enable_language(Fortran)
set(CMAKE_Fortran_COMPILER gfortran)

# Add the C library
add_library(plugin SHARED hello.c)

# Set the Fortran executable and link with the C library
add_executable(myprogram c_hello.f90)
target_link_libraries(myprogram plugin)

# Set the library search path to include the build directory
link_directories(${CMAKE_CURRENT_BINARY_DIR})

# Set the install directory for the executable and library
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_BINARY_DIR})
install(TARGETS myprogram DESTINATION bin)
install(TARGETS plugin DESTINATION lib)
