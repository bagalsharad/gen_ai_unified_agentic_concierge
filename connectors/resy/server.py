import grpc
from concurrent import futures
import time

# Placeholder for compiled protobuf
# import resy_pb2
# import resy_pb2_grpc

class ResyConnectorService: # (resy_pb2_grpc.ResyServiceServicer):
    def GetInventory(self, request, context):
        print(f"Fetching Resy inventory for: {request.location}")
        # return resy_pb2.InventoryResponse(...)
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # resy_pb2_grpc.add_ResyServiceServicer_to_server(ResyConnectorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Resy gRPC Connector started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
