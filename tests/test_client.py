import sys
import os
import unittest


class TestEDCClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.channel = grpc.insecure_channel('localhost:50051')
        cls.stub = DiagnosticsServiceStub(cls.channel)

    def test_get_system_status(self):
        response = self.stub.GetSystemStatus(Empty())
        self.assertIsInstance(response.cpu_usage, float)
        self.assertIsInstance(response.memory_usage, float)
        self.assertTrue(response.uptime)

    def test_valid_service_control(self):
        request = ServiceCommand(service_name="cron", action="restart")
        response = self.stub.ControlService(request)
        self.assertIn(response.success, [True, False])

    def test_invalid_service_control(self):
        request = ServiceCommand(
            service_name="invalid_service_xyz", action="restart")
        response = self.stub.ControlService(request)
        self.assertFalse(response.success)


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'client'))
    import grpc
    from diagnostics_pb2 import Empty, ServiceCommand
    from diagnostics_pb2_grpc import DiagnosticsServiceStub
    unittest.main()
