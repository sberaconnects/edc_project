SUMMARY = "EDC gRPC Diagnostics Daemon"
DESCRIPTION = "A lightweight embedded system diagnostics and service control daemon using gRPC"
LICENSE = "MIT"
SRC_URI = "file://src/main.cpp \
           file://src/diagnostics_service_impl.cpp \
           file://include/diagnostics_service_impl.h \
           file://CMakeLists.txt \
           file://../proto/diagnostics.proto \
           file://edc_daemon.service"

S = "${WORKDIR}"

DEPENDS = "grpc protobuf systemd"

inherit cmake systemd

SYSTEMD_SERVICE:${PN} = "edc_daemon.service"

do_configure:prepend() {
    mkdir -p ${S}/src
    mkdir -p ${S}/include
    cp ${WORKDIR}/main.cpp ${S}/src/
    cp ${WORKDIR}/diagnostics_service_impl.cpp ${S}/src/
    cp ${WORKDIR}/diagnostics_service_impl.h ${S}/include/
    cp ${WORKDIR}/CMakeLists.txt ${S}/
    cp ${WORKDIR}/diagnostics.proto ${S}/
}

do_install:append() {
    install -d ${D}${bindir}
    install -m 0755 edc_daemon ${D}${bindir}/edc_daemon

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/edc_daemon.service ${D}${systemd_system_unitdir}/edc_daemon.service
}
