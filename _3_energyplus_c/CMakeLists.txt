cmake_minimum_required(VERSION 3.0)

project(TestProject)

add_executable(test _test1.c)

target_include_directories(test PUBLIC /usr/local/EnergyPlus-23-1-0/include)
target_link_directories(test PUBLIC /usr/local/EnergyPlus-23-1-0)
target_link_libraries(test PUBLIC energyplusapi)

add_custom_target(run
    COMMAND ./test
    DEPENDS test
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

add_custom_target(clean-all
    COMMAND rm -rf CMakeFiles
    COMMAND rm -rf CMakeCache.txt
    COMMAND rm -rf Makefile
    COMMAND rm -rf cmake_install.cmake
    COMMAND rm -rf test
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

