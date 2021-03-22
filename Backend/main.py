import os
from flask import Flask
from flask import request, jsonify, send_from_directory, make_response, current_app
from flask_cors import CORS, cross_origin
import json
import numpy as np
from PIL import Image
import base64
import io
from datetime import timedelta
import functools
from flask_talisman import Talisman

cnxtSSL = ('./cert/certificate.crt','./cert/private.key')

app = Flask(__name__)
Talisman(app)
CORS(app, support_credentials=True)
app.url_map.strict_slashes = False


ROOT_DIR  = os.getcwd()

# os.chdir({ROOT_DIR+'/TFModels/research'})
# !protoc object_detection/protos/*.proto --python_out=.
# !python setup.py build
# !python setup.py install

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"

            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return functools.update_wrapper(wrapped_function, f)
    return decorator


from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format


# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(ROOT_DIR + '/Model/pipeline.config')
detection_model = model_builder.build(model_config=configs['model'], is_training=False)


# # Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(ROOT_DIR+'/Model/', 'ckpt-6')).expect_partial()


# @tf.function
def detect_fn(image):

    global detection_model
    
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    d = {
            "detection_boxes": detections['detection_boxes'].numpy().tolist(),
            "detection_classes": detections['detection_classes'].numpy().tolist(),
            "detection_scores": detections['detection_scores'].numpy().tolist()
        }

    return json.dumps(d,cls=NumpyEncoder)

# image_np = Image.open(ROOT_DIR + '/Data/test.jpg')
# input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
# detections = detect_fn(input_tensor)
# print(detections)


@app.route('/')
# @crossdomain(origin='*')
# @cross_origin(supports_credentials=True)
def hw():
    return jsonify({"code":200,"data": 'What\'s the sqrt of 13325?'})



@app.route('/<path:path>')
# @crossdomain(origin='*')
# @cross_origin(supports_credentials=True)
def hwf(path):
    if path != "":
        return send_from_directory('',path)
    else:
        return jsonify({"code":404,"data": 'file not found'})



@app.route('/predict', methods = ['GET', 'POST'])
# @crossdomain(origin='*')
# @cross_origin(supports_credentials=True)
def upload_file():
    print(request)
    if (request.method == 'POST' and request.json['img']):
        img = request.json['img']
        img = img.split('base64,')[1]        
        img = base64.b64decode(str(img))
        img = Image.open(io.BytesIO(img))        
        img = img.convert('RGB')
        img = np.asarray(img,dtype=np.float)

        # return jsonify({"code":201,"data": img.shape})
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(img, 0), dtype=tf.float32)
        d = detect_fn(input_tensor)
     
        response = jsonify({"code":200,"data": d})
        return response

    else:
        response = jsonify({"code":201,"data": 'Error'})
        return response


@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
    return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True, ssl_context = cnxtSSL )
    # app.run(host='0.0.0.0', port=80, debug=True )

