==========================================
Tensorflow gRPC and RESTful API Server
==========================================


tfserver is an example for serving Tensorflow model with `Skitai App Engine`_.

It can be accessed by gRPC and JSON RESTful API.


Saving Tensoflow Model
---------------------------

See `tf.saved_model.builder.SavedModelBuilder`_, but for example:

.. code:: python
  
  import dnn
  import tensorflow as tf
  
  net = dnn.build (phase_train=False)
  
  sess = tf.Session()
  sess.run (tf.global_variables_initializer())
  
  # restoring checkpoint
  saver = tf.train.Saver (tf.global_variables())
  saver.restore (sess, "./models/model.cpkt-1000")
  
  # save model with builder  
  builder = tf.saved_model.builder.SavedModelBuilde r("exported/1/")
  
  prediction_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
      inputs={'x': tf.saved_model.utils.build_tensor_info (net.x)},
      outputs={'y': tf.saved_model.utils.build_tensor_info (net.predict)])},
      method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)
  )  
  # Remember 'x', 'y' for I/O
  
  legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
  builder.add_meta_graph_and_variables(
    sess, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={'signature_def_name': prediction_signature},
    legacy_init_op=legacy_init_op
  )
  # Remember 'signature_def_name'
  
  builder.save()

.. _`tf.saved_model.builder.SavedModelBuilder`: https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/SavedModelBuilder
.. _`Skitai App Engine`: https://pypi.python.org/pypi/skitai


Run Tensorflow Server
------------------------

Example of api.py

.. code:: python
  
  import tfserver
  import skitai
  import tensorflow as tf

  pref = skitai.pref ()
  pref.config.tf_model_dir = "./exported/1"
  pref.config.tf_config = tf.ConfigProto(
    gpu_options=tf.GPUOptions (per_process_gpu_memory_fraction = 0.2), 
    log_device_placement = False
  )
  
  # If you want to activate gRPC, should mount /
  skitai.mount ("/", tfserver, pref = pref)
  skitai.run (port = 5000)

And run,

.. code:: bash

  python api.py  
  

gRPC Client
--------------

Using grpcio library,

.. code:: python

  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  import numpy as np
  
  stub = cli.Proxy ("localhost", 5000)
  problem = np.array ([1.0, 2.0])
  
  # put problem as 'x', and 'signature_def_name'
  # ignore 'model_name' for now
  resp = stub.predict (
    'model_name',
    'signature_def_name', 
    x = tensor_util.make_tensor_proto(problem.astype('float32'), shape=problem.shape)
  )
  # then get 'y'
  resp.y
  >> [-1.5, 1.6]

Using aquests for async request,

.. code:: python
  
  import aquests
  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  import numpy as np
  
  def print_result (resp):
    cli.Response (resp.data).y
    >> [-1.5, 1.6]
    
  stub = aquests.grpc ("http://localhost:5000", callback = print_result)
  problem = np.array ([1.0, 2.0])
  
  request = cli.build_request (
    'model_name',
    'signature_def_name', 
    x = tensor_util.make_tensor_proto(problem.astype('float32'), shape=problem.shape)
  )
  stub.Predict (request, 10.0)

  aquests.fetchall ()

But aquests' grpc is not stable yet.
  
RESTful API
-------------

Using requests,

.. code:: python
  
  import requests
  
  problem = np.array ([1.0, 2.0])
  api = requests.session ()
  resp = api.post (
    "http://localhost:5000/predict",
    json.dumps ({"x": problem.astype ("float32").tolist()}), 
    headers = {"Content-Type": "application/json"}
  )
  data = json.loads (resp.text)
  data ["y"]
  >> [-1.5, 1.6]

Another,
  
.. code:: python

  from aquests.lib import siesta
  
  problem = np.array ([1.0, 2.0])  
  api = siesta.API ("http://localhost:5000")
  resp = api.predict ().post ({"x": problem.astype ("float32").tolist()})
  resp.data.y  
  >> [-1.5, 1.6]

  
TODO
----------

- Multiple model serving


Release History
-------------------

- 0.1a (2018. 1. 4)

  - Alpha release
  