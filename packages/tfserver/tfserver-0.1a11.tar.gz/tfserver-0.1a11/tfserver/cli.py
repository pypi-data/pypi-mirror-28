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
		self.data = {}
		self.decode ()		
	
	def __getattr__ (self, name):
		return self.data.get (name)
		
	def decode (self):		
		for k, v in self.pb.outputs.items ():
			if isinstance (v, TensorProto):
				self.data [k] = tensor_util.MakeNdarray (v)
			else:
				self.data [k] = np.array (v.float_val)

class Proxy:
	def __init__ (self, host, port):
		self.host = host
		self.port = port
		channel = implementations.insecure_channel(host, port)
		self.stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
		
	def predict (self, spec_name, spec_signature_name, timeout = 10, **params):
		request = build_request (spec_name, spec_signature_name, **params)
		pred = self.stub.Predict (request, timeout)
		return Response (pred)

def build_request (spec_name, spec_signature_name,**params):	
	def _encode (obj):
		if not isinstance (obj, TensorProto):
			return tensor_util.make_tensor_proto(obj.astype('float32'), shape=obj.shape)
		return obj
		
	request = predict_pb2.PredictRequest()
	request.model_spec.name = spec_name
	request.model_spec.signature_name = spec_signature_name
	for k, v in params.items ():
		request.inputs [k].CopyFrom(_encode (v))
	return request