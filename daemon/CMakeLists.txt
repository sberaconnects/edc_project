cmake_minimum_required(VERSION 3.13)
project(edc_daemon)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

include_directories(${Protobuf_INCLUDE_DIRS} ../include)
include_directories(${CMAKE_CURRENT_BINARY_DIR})

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ../proto/diagnostics.proto)
grpc_generate_cpp(GRPC_SRCS GRPC_HDRS ../proto/diagnostics.proto)

add_executable(edc_daemon
    src/main.cpp
    src/diagnostics_service_impl.cpp
    ${PROTO_SRCS}
    ${GRPC_SRCS}
)

target_link_libraries(edc_daemon
    gRPC::grpc++
    protobuf::libprotobuf
)
