
cmake_minimum_required(VERSION 3.0)

project(myprogram)

# Set the Fortran compiler
enable_language(Fortran)
set(CMAKE_Fortran_COMPILER gfortran)

# Add the C libraries
add_library(plugin SHARED ephello.c)
find_library(ENERGYPLUS_API_LIBRARY NAMES energyplusapi HINTS /usr/local/EnergyPlus-23-1-0)
add_library(energyplusapi SHARED IMPORTED)
set_target_properties(energyplusapi PROPERTIES IMPORTED_LOCATION ${ENERGYPLUS_API_LIBRARY})
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -I/usr/local/EnergyPlus-23-1-0/include")

# Set the Fortran executable and link with the C libraries
add_executable(myprogram c_ep_hello.f90)
target_link_libraries(myprogram plugin energyplusapi)

# Set the library search path to include the build directory
link_directories(${CMAKE_CURRENT_BINARY_DIR})

# Set the install directory for the executable and library
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_BINARY_DIR})
install(TARGETS myprogram DESTINATION bin)
install(TARGETS plugin DESTINATION lib)
