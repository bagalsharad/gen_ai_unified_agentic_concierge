import grpc
from concurrent import futures
import time

class TockConnectorService:
    def GetInventory(self, request, context):
        print(f"Fetching Tock inventory for: {request.location}")
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Tock gRPC Connector started on port 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
