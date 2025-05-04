import grpc
import time
import argparse
import csv
from diagnostics_pb2 import Empty
from diagnostics_pb2_grpc import DiagnosticsServiceStub

def log_metrics(stub, interval, output):
    fieldnames = ["timestamp", "cpu_usage", "memory_usage", "uptime"]
    if output:
        f = open(output, 'w', newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    else:
        writer = None

    try:
        while True:
            response = stub.GetSystemStatus(Empty())
            row = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_usage": f"{response.cpu_usage:.2f}",
                "memory_usage": f"{response.memory_usage:.2f}",
                "uptime": response.uptime
            }
            if writer:
                writer.writerow(row)
                f.flush()
            else:
                print(row)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Logging stopped.")
    finally:
        if writer:
            f.close()

def main():
    parser = argparse.ArgumentParser(description="EDC Metrics Logger")
    parser.add_argument('--interval', type=int, default=5)
    parser.add_argument('--output', help='Output CSV file')
    args = parser.parse_args()

    channel = grpc.insecure_channel('localhost:50051')
    stub = DiagnosticsServiceStub(channel)
    log_metrics(stub, args.interval, args.output)

if __name__ == '__main__':
    main()
