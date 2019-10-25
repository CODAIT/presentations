#
# Copyright 2018 IBM Corp. All Rights Reserved.
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

from flask import Flask, render_template, request
import argparse
import requests
import cv2
import logging
import numpy as np
import os
import glob
from pprint import pformat
from random import randint
from PIL import Image

# setup logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

# parse port and model endpoint args
parser = argparse.ArgumentParser(description='MAX Fashion MNIST')
parser.add_argument('--port', type=int, nargs='?', default=8090,
                    help='port to run the web app on')
parser.add_argument('--ml-endpoint', nargs='?', metavar='URL',
                    default='http://localhost:5000', help='model api server')
args = parser.parse_args()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def root():

    # removing all previous files in folder before start processing
    output_folder = 'static/img/temp/'
    for file in glob.glob(output_folder + '*'):
        os.remove(file)

    # on POST handle upload
    if request.method == 'POST':

        # get file details
        file_data = request.files.get('file')
        if file_data is None:
            err_msg = 'No input image was provided.'
            logging.error(err_msg)
            return render_template('index.html', error_msg=err_msg)


        # read image from string data
        file_request = file_data.read()
        # convert string data to numpy array
        np_inp_image = np.fromstring(file_request, np.uint8)
        img = cv2.imdecode(np_inp_image, cv2.IMREAD_UNCHANGED)
        _, image_encoded = cv2.imencode('.jpeg', img)

        # TODO R1: review inference request payload
        # Required inference request parameter: image (JPG/PNG encoded)
        files = {
            'file': image_encoded.tostring(),
            'Content-Type': 'multipart/form-data',
        }

        # TODO T1: replace model URL placeholder
        # Add model endpoint
        model_url = args.ml_endpoint.rstrip('/') + '/model/predict'

        # Send image file form to model endpoint for prediction
        try:
            results = requests.post(url=model_url, files=files)
        except Exception as e:
            err_msg_temp = 'Prediction request to {} failed: {}'
            err_msg = err_msg_temp.format(model_url, 'Check log for details.')
            logging.error(err_msg_temp.format(model_url, str(e)))
            return render_template("index.html", error_msg=err_msg)

        # surface any prediction errors to user
        if results.status_code != 200:
            err_msg = ('Prediction request returned status code {} '
                       + 'and message {}').format(results.status_code,
                                                  results.text)
            logging.error(err_msg)
            return render_template('index.html', error_msg=err_msg)

        # extract prediction from json return
        output_data = results.json()

        # log output in debug
        logging.debug('\n' + pformat(output_data))

        # TODO T2: replace placeholder with appropriate JSON key
        # Extraction prediction result
        result = output_data['predictions']

        if len(result) == 0:
            msg = 'No objects detected, try uploading a new image'
            return render_template('index.html', error_msg=msg)
        else:

            # save the output image to return
            file_name = (str(randint(0, 999999)) + '.jpg')
            output_name = output_folder + '/' + file_name
            im = Image.fromarray(img)
            im = im.convert("L")
            newsize = (300, 300)
            im = im.resize(newsize)
            im.save(output_name)

        return render_template('index.html', image_name=output_name, result_1=result[0]['prediction'])

    else:
        # on GET return index.html
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=args.port)
