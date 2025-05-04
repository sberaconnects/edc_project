# Embedded Diagnostics Console (EDC)

A lightweight, modular **embedded diagnostics and control system** using **gRPC** for IPC, written in C++ with a Python CLI client.

EDC runs as a background daemon on embedded Linux (e.g., Raspberry Pi, Yocto systems) and exposes system status and control operations such as service restarts via a well-defined gRPC API.

---

## 📌 Features

- 🧠 **Modular C++ Daemon** with gRPC support
- 🛠️ Real-time system monitoring (CPU, memory, uptime)
- 📡 Remote systemd service control (start/stop/restart)
- 🐍 Python CLI to interact with the daemon
- 📈 Metrics logger tool to log data over time
- ⚙️ Integrated with **systemd**
- 🧪 Fully testable with Python `unittest`
- 🧩 Yocto layer & recipe for embedded deployment
- 🔐 Extensible for MQTT, Prometheus, REST, or Web UI

---

## 🧱 Architecture

```
Python CLI / Tools
        │
   gRPC via Protobuf
        │
+------------------------+
|  C++ gRPC Daemon       |
|  - DiagnosticsService  |
|  - System Monitor      |
|  - Service Control     |
+------------------------+
        │
Embedded Linux (Yocto or Fedora)
```

---

## 🚀 Quick Start

### 1. Build the C++ Daemon

```bash
mkdir build && cd build
cmake ../daemon
make
```

🛠️ **Note:** Make sure the include path is set correctly. The CMakeLists.txt uses:
```cmake
include_directories(${Protobuf_INCLUDE_DIRS} ./include ../proto)
```

### 2. Run the Server

```bash
./edc_daemon
```

### 3. Use the Python CLI

```bash
# Install dependencies
pip install grpcio grpcio-tools

# Generate gRPC bindings
python -m grpc_tools.protoc -I./proto --python_out=client --grpc_python_out=client ./proto/diagnostics.proto

# Run CLI
python client/cli.py status
python client/cli.py control --service crond --action restart
```

---

## 📊 Log Metrics

```bash
python tools/metrics_logger.py --interval 3 --output metrics.csv
```

---

## 🧪 Run Tests

```bash
python tests/test_client.py
```

---

## 🧰 Yocto Integration

1. Add `meta-edc` to your `bblayers.conf`
2. Append to `local.conf`:
   ```bash
   IMAGE_INSTALL:append = " edc-daemon"
   ```
3. Build your image with:
   ```bash
   bitbake core-image-minimal
   ```

---

## 📂 Project Structure

```
edc_project/
├── client
│   └── cli.py
├── daemon
│   ├── CMakeLists.txt
│   ├── include
│   │   └── diagnostics_service_impl.h
│   └── src
│       ├── diagnostics_service_impl.cpp
│       └── main.cpp
├── proto
│   └── diagnostics.proto
├── README.md
├── systemd
│   └── edc_daemon.service
├── tests
│   └── test_client.py
├── tools
│   └── metrics_logger.py
└── yocto-layer
    └── meta-edc
        └── recipes-edc
            └── edc-daemon
                ├── edc-daemon_1.0.bb
                └── edc_daemon.service

13 directories, 12 files

```

---

## 📌 License

MIT License — Free to use, fork, and extend!

---

## 🙋‍♂️ Author

Built by **Sudhir Kumar Bera** – Senior Embedded Software Engineer | C++ | Yocto | Systemd | gRPC | Linux

Connect on [LinkedIn](www.linkedin.com/in/sudhir-bera-77a13215)