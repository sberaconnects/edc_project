# Stage 1: Build
FROM fedora:42 as builder

# Install build tools and gRPC dependencies
RUN dnf install -y cmake gcc-c++ make \
    grpc-devel grpc-plugins \
    protobuf protobuf-compiler protobuf-devel \
    abseil-cpp-devel

WORKDIR /app

# Copy project files
COPY daemon /app/daemon
COPY proto /app/proto

# Configure and build
RUN mkdir build && cd build && \
    cmake ../daemon && \
    make -j$(nproc)

# Stage 2: Runtime
FROM fedora:42

# Copy the built daemon binary
COPY --from=builder /app/build/edc_daemon /usr/local/bin/edc_daemon

EXPOSE 50051

ENTRYPOINT ["/usr/local/bin/edc_daemon"]
