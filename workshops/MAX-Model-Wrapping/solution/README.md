[![Build Status](https://travis-ci.com/IBM/MAX-Skeleton.svg?branch=master)](https://travis-ci.com/IBM/MAX-Skeleton)

# Model Asset Exchange Scaffolding

Docker based deployment skeleton for deep learning models on the Model Asset Exchange.

## Prerequisites:

* You will need Docker installed. Follow the [installation instructions](https://docs.docker.com/install/) for your
system.
* Have the model saved in SavedModel format and uploaded to a public [Cloud Object Storage](https://console.bluemix.net/catalog/services/cloud-object-storage) bucket.

## Step-by-step Guide to Wrapping a Model

### 1. Clone the skeleton
Clone the `MAX-skeleton` repository locally. In a terminal run the following command:
```bash
$ git clone https://github.com/IBM/MAX-Skeleton
```
The project files are structured into three main parts: model, api, and samples. The `model` directory will contain code used for loading the model and running the predictions. The `api` directory contains code to handle the inputs and outputs of the MAX microservice. The `samples` directory will contain sample data and notebooks for the user to try the service.

Example:
```
./
  app.py
  model/
    model.py
  api/
    metadata.py
    predict.py
```

### 2. Modify the Dockerfile
In the [`Dockerfile`](Dockerfile) we need to modify the following `ARG` instructions with a link to the
public object storage bucket and the name of the file containing the serialized model.

    ARG model_bucket=
    ARG model_file=

Then, calculate and add the SHA512 hashes of the files that will be downloaded to `sha512sums.txt`. Note: the hashes should be
of the files after any extraction (eg after un-taring or un-ziping).

To calculate the SHA512 sum of a file run:
```bash
$ sha512sum <FILE NAME>
```

### 3. Import the model in `core/model.py`

This is where we handle the framework specific code for running predictions. The model is
loaded in the `ModelWrapper.__init__()` method. Any code that needs to run when
the model is loaded is also placed here.

There are also separate functions for pre-processing, predictions, and post-processing that need to be implemented. The  `MAXModelWrapper` base class has a default `predict` method that internally calls these pre-processing, prediction, and post-processing functions.
The model metadata should also be defined here.

```python
class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': 'ID',
        'name': 'MODEL NAME',
        'description': 'DESCRIPTION',
        'type': 'MODEL TYPE',
        'source': 'MODEL SOURCE'
        'license': 'LICENSE'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        pass

    def _pre_process(self, inp):
        return inp

    def _post_process(self, result):
        return result

    def _predict(self, x):
        return x
```

### 4. Add input/output parsing code in `api/predict.py`

The input and outputs requests are sent as JSON strings. We define the format of these requests using the `flask_restplus` package. In the skeleton we have the output response configured with the following schema:

```json
{
    "predictions": [
        {
            "probability": "float",
            "label": "string",
            "label_id": "string"
        },
    ],
    "status": "string"
}
```
The `predict_response` and `label_prediction` variables can be modified to amend the schema for each model's specific response format.

To define the input format for a prediction we use Flask-RESTPlus's request parsing interface. The default input takes in a file.

### 5. Create MAXApp instance in `app.py`

The following code is already in the skeleton, but you may need to manually add extra APIs if needed.
```python
from maxfw.core import MAXApp
from api import ModelMetadataAPI, ModelPredictAPI
from config import API_TITLE, API_DESC, API_VERSION

max = MAXApp(API_TITLE, API_DESC, API_VERSION)
max.add_api(ModelMetadataAPI, '/metadata')
max.add_api(ModelPredictAPI, '/predict')
max.run()
```

### 6. Add integration tests

Add a few integration tests using `pytest` in `tests/test.py` to check that your model works. To enable Travis CI
testing uncomment the `docker` commands and `pytest` command in `.travis.yml`.

### 7. Add requirements

Add required python packages to `requirements.txt`

## Testing Out the Model with Docker

### 1. Build the model Docker image

To build the docker image locally, run:

```bash
$ docker build -t max-model .
```

If you want to print debugging messages make sure to set `DEBUG=True` in `config.py`.

### 2. Run the model server

To run the docker image, which automatically starts the model serving API, run:

```bash
$ docker run -it -p 5000:5000 max-model
```

### 3. Test the API

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test file and get a response from the API.

```bash
$ curl -F "file=@<INPUT_FILE_PATH>" -XPOST http://localhost:5000/model/predict
```

### 4. Run the Test Cases

Install test required packages and run tests using `pytest`:

```bash
$ pip install -r requirements-test.txt
$ pytest tests/test.py
```

## Provide documentation

Copy the README files and add the relevant details for the specific model and use case, following the MAX standard. See other MAX models (e.g. [Object Detector](https://github.com/IBM/MAX-Object-Detector)) for examples. 

More specifically, update the following README files:
- Replace this `README.md` file with the completed `README-template.md` file
- Complete the `samples/README.md` file with information about the data samples and the demo notebook, if any
