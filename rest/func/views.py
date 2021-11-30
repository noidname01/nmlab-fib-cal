from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import os.path as osp

# read config file
import configparser
config = configparser.ConfigParser()

CONFIG_PATH = osp.join(osp.dirname(osp.abspath(__file__)), "../../config.ini")
config.read(CONFIG_PATH)
config = config["DEFAULT"]

# for gRPC
import grpc
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC/build/service")
sys.path.insert(0, BUILD_DIR)
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc
from google.protobuf.json_format import MessageToDict

# for MQTT
import paho.mqtt.client as mqtt

class FibView(APIView):
    permissions_classes = (permissions.AllowAny,)
    

    def post(self, request):
        host = f"{config['IP']}:{config['GRPC_PORT']}"
        order = request.POST['order']
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            grpc_request = fib_pb2.FibRequest()
            grpc_request.order = int(order)

            grpc_response = stub.Compute(grpc_request)

        mqtt_client = mqtt.Client()
        mqtt_client.connect(host=config['IP'], port=int(config['MQTT_PORT']))
        mqtt_client.loop_start()
        mqtt_client.publish(topic=config['HISTORY_TOPIC'], payload=order)
        return Response(data={"value":grpc_response.value}, status=200)

class LogsView(APIView):
    permissions_classes = (permissions.AllowAny,)

    def get(self, request):
        host = f"{config['IP']}:{config['GRPC_PORT']}"
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LogsStub(channel)
            grpc_request = log_pb2.LogsRequest()
            grpc_response = stub.Log(grpc_request)

            history = (MessageToDict(grpc_response))

        return Response(data=history, status=200)