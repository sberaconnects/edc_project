SUMMARY = "Embedded Diagnostics Console Daemon"
DESCRIPTION = "gRPC-based diagnostics daemon with systemd support"
LICENSE = "MIT"
SRC_URI = "file://main.cpp file://diagnostics_service_impl.cpp file://CMakeLists.txt file://diagnostics.proto file://edc_daemon.service"
S = "${WORKDIR}"
DEPENDS = "grpc protobuf systemd"
inherit cmake systemd
SYSTEMD_SERVICE:${PN} = "edc_daemon.service"
do_install:append() {
    install -d ${D}${bindir}
    install -m 0755 edc_daemon ${D}${bindir}/edc_daemon
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/edc_daemon.service ${D}${systemd_system_unitdir}
}
