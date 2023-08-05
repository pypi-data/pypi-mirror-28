#!/usr/bin/env python

# This is a placeholder for a Google-internal import.
import time
from grpc.beta import implementations
import tensorflow as tf
import numpy as np
from tensorflow.python.framework import tensor_util
from tensorflow.core.framework.tensor_pb2 import TensorProto
from . import prediction_service_pb2, predict_pb2

class Response:
	def __init__ (self, pb):
		self.pb = pb
		self.y = self.decode ()
	
	def decode (self):
		y = self.pb.outputs ["y"]
		if isinstance (y, TensorProto):
			return tensor_util.MakeNdarray (y)
		else:
			np.array (y.float_val)	


class Proxy:
	def __init__ (self, host, port):
		self.host = host
		self.port = port
		channel = implementations.insecure_channel(host, port)
		self.stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
			
	def predict (self, spec_name, spec_signature_name, x, timeout = 10):
		request = predict_pb2.PredictRequest()
		request.model_spec.name = spec_name
		request.model_spec.signature_name = spec_signature_name
		request.inputs ["x"].CopyFrom(x)
		pred = self.stub.Predict (request, timeout)
		return Response (pred)
