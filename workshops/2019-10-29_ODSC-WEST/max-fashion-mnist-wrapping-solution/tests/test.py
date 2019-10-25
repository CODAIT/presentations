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

import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX FASHION ' \
                                                                 'MNIST - Fashion ' \
                                                                 'and Clothing items ' \
                                                                 'Classification'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'Image Classification'
    assert metadata['name'] == 'MAX-Fashion-MNIST'
    assert metadata['description'] == 'Classify clothing and fashion items'
    assert metadata['license'] == 'Apache 2.0'


def test_response():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/1.jpeg'

    with open(file_path, 'rb') as file:
        file_form = {'file': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    print(r.content)
    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'

    # add sanity checks here
    assert response['predictions'][0]['prediction'] == "T-shirt/top"


if __name__ == '__main__':
    pytest.main([__file__])
