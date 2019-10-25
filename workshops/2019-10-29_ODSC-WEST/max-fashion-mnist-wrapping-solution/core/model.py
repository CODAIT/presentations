#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from maxfw.model import MAXModelWrapper

from PIL import Image
import numpy as np
import io
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

import logging
from config import DEFAULT_MODEL_PATH, CLASS_DIGIT_TO_LABEL

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': 'Image Classification',
        'name': 'MAX-Fashion-MNIST',
        'description': 'Classify clothing and fashion items',
        'type': 'TensorFlow model',
        'source': 'https://github.com/SSaishruthi/max_fashion_mnist',
        'license': 'Apache 2.0'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        # Load the model
        global sess
        global graph
        sess = tf.Session()
        graph = tf.get_default_graph()
        set_session(sess)
        self.model = tf.keras.models.load_model(path)
        logger.info('Loaded model')

    def _pre_process(self, inp):
        # Open the input image
        img = Image.open(io.BytesIO(inp))
        # Convert the PIL image instance into numpy array and
        # get in proper dimension.
        image = tf.keras.preprocessing.image.img_to_array(img)
        image = np.expand_dims(image, axis=0)
        return image

    def _post_process(self, result):
        # Extract prediction probability using `amax` and
        # digit prediction using `argmax`
        return [{'probability': np.amax(result),
                 'prediction': CLASS_DIGIT_TO_LABEL[np.argmax(result)]}]

    def _predict(self, x):
        with graph.as_default():
            set_session(sess)
            predict_result = self.model.predict(x)
            return predict_result
