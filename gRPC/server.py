import os.path as osp
import sys
import threading
# read config file
import configparser
config = configparser.ConfigParser()

CONFIG_PATH = osp.join(osp.dirname(osp.abspath(__file__)), "../config.ini")
config.read(CONFIG_PATH)
config = config["DEFAULT"]

BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)

import grpc
from concurrent import futures
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

history_record = []

class FibCalculatorServicer(fib_pb2_grpc.FibCalculatorServicer):

    def __init__(self):
        pass

    def Compute(self, request, context):
        n = request.order
        value = self._fibonacci(n)

        response = fib_pb2.FibResponse()
        response.value = value

        return response

    def _fibonacci(self, n):
        a = 0
        b = 1
        if n < 0:
            return 0
        elif n == 0:
            return 0
        elif n == 1:
            return b
        else:
            for i in range(1, n):
                c = a + b
                a = b
                b = c
            return b

class LogsServicer(log_pb2_grpc.LogsServicer):
    
    def __init__(self):
        pass

    

    def Log(self, request, context):
        response = log_pb2.LogsResponse()
        response.history[:] = history_record

        return response


def on_message(client, obj, msg):
    history_record.append(int(msg.payload.decode()))

def mqtt_subscribe():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host=config['IP'], port=int(config['MQTT_PORT']))
    client.subscribe(config['HISTORY_TOPIC'], 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fib_servicer = FibCalculatorServicer()
    log_servicer = LogsServicer()
    fib_pb2_grpc.add_FibCalculatorServicer_to_server(fib_servicer, server)
    log_pb2_grpc.add_LogsServicer_to_server(log_servicer, server)

    try:
        server.add_insecure_port(f"{config['IP']}:{config['GRPC_PORT']}")
        server.start()
        print(f"Run gRPC Server at {config['IP']}:{config['GRPC_PORT']}")
        
        t = threading.Thread(target=mqtt_subscribe)
        t.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass