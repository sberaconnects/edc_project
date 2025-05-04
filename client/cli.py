import grpc
import argparse
from diagnostics_pb2 import Empty, ServiceCommand
from diagnostics_pb2_grpc import DiagnosticsServiceStub

def get_status(stub):
    response = stub.GetSystemStatus(Empty())
    print("CPU Usage     :", response.cpu_usage, "%")
    print("Memory Usage  :", response.memory_usage, "%")
    print("Uptime        :", response.uptime)

def control_service(stub, name, action):
    request = ServiceCommand(service_name=name, action=action)
    response = stub.ControlService(request)
    print("Result:", "✅ Success" if response.success else "❌ Failed")
    print("Message:", response.message)

def main():
    parser = argparse.ArgumentParser(description="EDC Client CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('status', help="Get system status")
    control_cmd = subparsers.add_parser('control', help="Control a systemd service")
    control_cmd.add_argument('--service', required=True)
    control_cmd.add_argument('--action', required=True, choices=["start", "stop", "restart"])

    args = parser.parse_args()
    channel = grpc.insecure_channel('localhost:50051')
    stub = DiagnosticsServiceStub(channel)

    if args.command == 'status':
        get_status(stub)
    elif args.command == 'control':
        control_service(stub, args.service, args.action)

if __name__ == '__main__':
    main()
