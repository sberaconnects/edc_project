cmake_minimum_required(VERSION 3.13)
project(edc_daemon)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS} ./include ../proto)

# Compile .proto to .pb.cc/.pb.h
execute_process(
  COMMAND protoc --cpp_out=${CMAKE_CURRENT_BINARY_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
          --plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin
          -I ${CMAKE_CURRENT_SOURCE_DIR}/../proto diagnostics.proto
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../proto
)

set(PROTO_SRC
  ${CMAKE_CURRENT_BINARY_DIR}/diagnostics.pb.cc
  ${CMAKE_CURRENT_BINARY_DIR}/diagnostics.grpc.pb.cc
)

add_executable(edc_daemon
  src/main.cpp
  src/diagnostics_service_impl.cpp
  ${PROTO_SRC}
)

target_include_directories(edc_daemon PRIVATE
  ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(edc_daemon
    grpc++
    protobuf
    absl_synchronization
    absl_time
    absl_strings
)
