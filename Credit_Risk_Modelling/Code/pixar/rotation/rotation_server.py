import time
import grpc
from concurrent import futures
from autogenerated_files import rotation_model_pb2_grpc \
    as rotation_model_pb2_grpc
from src import rotation_service as rotator



_ONE_DAY_IN_SECONDS = 0

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    rotation_model_pb2_grpc.add_rotation_serviceServicer_to_server(rotator.Rotation(),server)
    server.add_insecure_port('[::]:50055')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    print("Server started with port 50055 ")
    serve()
