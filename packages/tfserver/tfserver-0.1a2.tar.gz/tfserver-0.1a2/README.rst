==========================================
Tensorflow gRPC and RESTful API Server
==========================================


Tensorflow Server
----------------------

Save this script to app.py

..code: python
  
  import tfserver
  import skitai
  import dnn
  import tensorflow as tf

  pref = skitai.pref ()
  
  pref.debug = True
  pref.use_reloader = True

  tf.reset_default_graph()
  net = dnn.make_mlp_network(tf, phase_train=False)

  pref.config.tf_config = tf.ConfigProto(
    gpu_options=tf.GPUOptions (per_process_gpu_memory_fraction = 0.2), 
    log_device_placement = False
  )
  pref.config.tf_model_dir = "./exported/2"
  pref.config.tf_predict_op = net ["pred"]
  pref.config.tf_x= net ["x"]

  skitai.mount ("/", tfserver, pref = pref)
  skitai.run (port = 5000)


gRPC Client
--------------

Using grpc,

..code: python

  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  
  stub = cli.Proxy ("localhost", 5000)
  x = np.array ([1.0, 2.0])

  resp = stub.predict (
    'model_name',
    'signature_name', 
    tensor_util.make_tensor_proto(x.astype('float32'), shape=x.shape)
  )
  resp.y
  >> [-1.5, 1.6]


Using aquests,

..code: python
  
  from tfserver import predict_pb2, cli
  import aquests
  from tensorflow.python.framework import tensor_util
  
  def print_result (resp):
    cli.Response (resp.data).y
    >> [-1.5, 1.6]
    
  stub = aquests.grpc ("http://localhost:5000", callback = print_result)
  x = np.array ([1.0, 2.0])

  request = predict_pb2.PredictRequest()
  request.model_spec.name = 'model_name'
  request.model_spec.signature_name = 'signature_name'
  request.inputs ["x"].CopyFrom(tensor_util.make_tensor_proto(fftseq.astype('float32'), shape=fftseq.shape))
  stub.Predict (request, 10.0)


REST API
----------

Using requests,

..code: python
  
  import requests
  
  api = requests.session ()
  resp = api.post (
    "http://localhost:5000/predict",
    json.dumps ({"x": getone ().astype ("float32").tolist()}), 
    headers = {"Content-Type": "application/json"}
  )
  data = json.loads (resp.text)
  data ["y"]
  >> [-1.5, 1.6]

Another,
  
..code: python

  from aquests.lib import siesta
  
  x = np.array ([1.0, 2.0])
  
  api = siesta.API ("http://localhost:5000")
  resp = api.predict ().post ({"x": x.astype ("float32").tolist()})
  resp.data.y  
  >> [-1.5, 1.6]
