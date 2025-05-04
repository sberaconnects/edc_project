#include "diagnostics_service_impl.h"
#include "diagnostics.grpc.pb.h"
#include <grpcpp/grpcpp.h>
#include <fstream>
#include <sstream>
#include <cstdlib>

using edc::CommandResult;
using edc::DiagnosticsService;
using edc::Empty;
using edc::ServiceCommand;
using edc::SystemStatus;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class DiagnosticsServiceImpl final : public DiagnosticsService::Service
{
public:
    Status GetSystemStatus(ServerContext *, const Empty *, SystemStatus *reply) override
    {
        std::ifstream meminfo("/proc/meminfo");
        float totalMem = 0, freeMem = 0;
        std::string line;
        while (getline(meminfo, line))
        {
            if (line.find("MemTotal") != std::string::npos)
                sscanf(line.c_str(), "MemTotal: %f", &totalMem);
            else if (line.find("MemAvailable") != std::string::npos)
                sscanf(line.c_str(), "MemAvailable: %f", &freeMem);
        }
        float memUsage = 100.0f - (freeMem / totalMem) * 100.0f;
        reply->set_cpu_usage(12.5);
        reply->set_memory_usage(memUsage);
        reply->set_uptime("123456s");
        return Status::OK;
    }

    Status ControlService(ServerContext *, const ServiceCommand *request, CommandResult *response) override
    {
        std::string command = "systemctl " + request->action() + " " + request->service_name();
        int result = system(command.c_str());
        response->set_success(result == 0);
        response->set_message(result == 0 ? "Success" : "Failed to execute systemctl");
        return Status::OK;
    }
};

void RunServer()
{
    std::string server_address("0.0.0.0:50051");
    DiagnosticsServiceImpl service;
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}
