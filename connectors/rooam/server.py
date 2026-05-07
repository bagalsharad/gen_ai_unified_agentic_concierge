import grpc
from concurrent import futures
import time

class RooamConnectorService:
    def GetUserTransactions(self, request, context):
        print(f"Fetching Rooam transactions for user: {request.user_id}")
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Rooam gRPC Connector started on port 50053")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
