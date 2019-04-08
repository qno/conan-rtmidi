cmake_minimum_required(VERSION 2.8.12)
project(RtMidiTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(rtmiditest rtmiditest.cpp)
target_link_libraries(rtmiditest ${CONAN_LIBS})
