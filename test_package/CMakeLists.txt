cmake_minimum_required (VERSION 3.5)
project (RtMidiTest)

include (${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable (rtmiditest rtmiditest.cpp)
conan_target_link_libraries (rtmiditest)
