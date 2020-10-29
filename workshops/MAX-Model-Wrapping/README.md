
:exclamation: Join the discussion on slack using this [link](http://ibm.biz/max-slack-invite). :exclamation:

# MAX-Fashion-MNIST

#### Classify fashion and clothing items. 

<div align="center">
  <img src="https://github.com/SSaishruthi/max-fashion-mnist/raw/master/samples/data.png" height="400" width="400">
</div>

# Data Source: 

IBM Developer - [Data Asset Exchange](https://developer.ibm.com/exchanges/data/)

Curated free and open datasets under open data licenses for enterprise data science.

Link to download: https://developer.ibm.com/exchanges/data/all/fashion-mnist/

# Model Framework

The model is developed using the [Tensorflow](https://www.tensorflow.org/) framework.

# Labels
Each training and test example is assigned to one of the following labels:

| Label | Description |
| --- | --- |
| 0 | T-shirt/top |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle boot |

# Training (Optional)

Model training code is available [here](https://github.com/CODAIT/presentations/blob/master/workshops/MAX-Model-Wrapping/training/Fashion_MNIST.ipynb).

Trained model has been saved to `fashion_mnist.h5`. Note this file name as we will use this in the microservice creation.

### Bonus

To directly use the training notebook as a Watson Studio project, click on `Run notebooks in Watson Studio` [here](https://dax-nb-preview-prod.s3.us.cloud-object-storage.appdomain.cloud/preview_notebooks.html?dataset=fashion-mnist).

To add [this](https://github.com/CODAIT/presentations/blob/master/workshops/MAX-Model-Wrapping/training/Fashion_MNIST.ipynb) training notebook to an existing Watson Studio project, follow steps under `Run the notebook` section in [this](https://developer.ibm.com/technologies/data-science/tutorials/getting-started-with-the-data-asset-exchange/) tutorial.

# Requirements

1. Pre-trained model stored in a downloadable location and sha512sum value for the model files.
2. Python IDE or code editors.
3. List of required python packages to run the scripts with their respective version numbers. 
4. Code to load the model
5. Input pre-processing code
6. Prediction/Inference code
7. Decide on output response and variables.
8. Output post-processing code
9. Docker to run the model microservice.

# Steps

1. [Fork the Template and Clone the Repository](#fork-the-template-and-clone-the-repository)
2. [Update Dockerfile](#update-dockerfile)
3. [Update Package Requirements](#update-package-requirements)
4. [Update API and Model Metadata](#update-api-and-model-metadata)
5. [Update Scripts](#update-scripts)
6. [Build the model Docker image](#build-the-model-docker-image)
7. [Run the model server](#run-the-model-server)

## Fork the Template and Clone the Repository

### Users with GitHub account

1. Login to GitHub and go to [MAX Skeleton](https://github.com/IBM/MAX-Skeleton)

2. Click on `Use this template` and provide a name for the repo.

3. Clone the newly created repository using the below command:

```bash
$ git clone https://github.com/[NEW REPO]

```

### Users without Github account

1. Clone the [MAX Skeleton](https://github.com/IBM/MAX-Skeleton) repository using the below the command:

```bash
$ git clone https://github.com/IBM/MAX-Skeleton.git
```

## Update Dockerfile

   Navigate to the folder you just cloned, open the Dockerfile file and update the following:

- `ARG model_bucket=` with the link to the model file public storage that can be downloaded.
   
- `ARG model_file=` with the model file name. 

   For testing purpose, uncomment `ARG model_bucket` and `ARG model_file` line and update as below:

```docker
ARG model_bucket=https://max-cdn.cdn.appdomain.cloud/max-wrapping-demo/1.0.0

ARG model_file=assets.tar.gz 
```

-  When building the Dockerfile, the integrity of the downloaded model file will be verified. If you're using the model file provided by us, the checksum in the `sha512sums.txt` file has to be replaced with the following:

```
51b54f16fe95b6d557c30908e3b5cdcb60d35ae1cf6cdb8651bcd2920abbddbe2c9b5d51c65ef0538fb9c8b0258ce0cf9afd2ba86c956d65ec3b1fef7a797485 assets/fashion_mnist.h5
```

## Update Package Requirements

Add required python packages for running the model prediction to `requirements.txt`. 

Following packages are required for this model:

```
tensorflow==1.15.2
numpy==1.16.1
Pillow==5.4.1
h5py==2.9.0
```
   

## Update API and Model Metadata

1. In `config.py`, update the API metadata. 

    This metadata is used to characterize the API wrapping the model.

   - API_TITLE 
   - API_DESC 
   - API_VERSION 

2. Set `MODEL_NAME = 'fashion_mnist.h5'`
 
   This is the user provided name for the trained model. [Refer](#training-optional) 

   _NOTE_: Model files are always downloaded to `assets` folder inside docker.

3. In `core/model.py`, fill in the `MODEL_META_DATA` 

    This metadata is used to characterize the model itself.
       
   - `id` of the model: this can be anything, e.g. `Image Classification`
   - `name` of the model: e.g. `MAX-Fashion-MNIST`
   - `description` of the model: e.g. `Classify clothing and fashion items`
   - `type` of the model based on what it's purpose is: e.g. `Image Classification`
   - `source` of the model: e.g. a url to the repository where this code will be stored.
   - `license` related to the source code: e.g. `Apache 2.0` if applicable
   
## Update Scripts

All you need to start wrapping your model is pre-processing, post-processing and prediction code.
  
1. In `core/model.py`, load the model under the `__init__()` method of the `ModelWrapper` class. 
   
    Here, the saved model (`.h5` format) can be loaded using the command below.
    
    ```python
    global sess
    global graph
    sess = tf.Session() 
    graph = tf.get_default_graph()
    set_session(sess)
    self.model = tf.keras.models.load_model(path)
    ```

    In order for the above to function, we will have to add the following dependency to the top of the file.

    ```python
    import tensorflow as tf
    from tensorflow.keras.backend import set_session
    ```


2. In `core/model.py`, input pre-processing functions should be placed under the `_pre_process` function.
   
    Here, the input image needs to be read and converted into an array of acceptable shape.
    
    _NOTE_: Remove `return inp` and add the below code.
  
    ```python
    # Open the input image
    img = Image.open(io.BytesIO(inp))
    print('reading image..', img.size)
    # Convert the PIL image instance into numpy array and
    # get in proper dimension.
    image = tf.keras.preprocessing.image.img_to_array(img)
    print('image array shape..', image.shape)
    image = np.expand_dims(image, axis=0)
    print('image array shape..', image.shape)
    return image
    ```

    In order for the above to function, we will have to add the following dependency to the top of the file.

    ```python
    import io
    import numpy as np
    from PIL import Image
    ```
 
3. Following pre-processing, we will feed the input to the model. Place the inference code under the `_predict` method in `core/model.py`. The model will return a list of class probabilities, corresponding to the likelihood of the input image to belong to respective class. There are 10 classes (digit 0 to 9), so `predict_result` will contain 10 values.
  
    _NOTE_: Remove `return x` and add the below code.
    
    ```python
    with graph.as_default():
      set_session(sess)
      predict_result = self.model.predict(x)
      return predict_result
    ```
     
4. The predicted class and it's probability are the desired output. In order to return these values in the API, we need to add these two fields to `label_prediction` in `api/predict.py`.
  
   Remove the below line in `label_prediction`.
   
   ```python
   'label_id': fields.String(required=False, description='Label identifier'),
   ```
   
   Replace `label` with `prediction` in `label_prediction`.
   
   ```python
    label_prediction = MAX_API.model('LabelPrediction', {
      'prediction': fields.String(required=True),
      'probability': fields.Float(required=True)
    })
    ```

    In addition, the output response has two fields `status` and `predictions` need to be updated as follows. This defines the format the API expects the output to be in.
  
    ```python
    predict_response = MAX_API.model('ModelPredictResponse', {
      'status': fields.String(required=True, description='Response status message'),
      'predictions': fields.List(fields.Nested(label_prediction), description='Predicted labels and probabilities')
    })
    ```
 
    _NOTE_: These fields can vary depending on the model.
    
5. Following inference, a post-processing step is needed to reformat the output of the `_predict` method. It's important to make sense of the results before returning the output to the user. Any post-processing code will go under the `_post_process` method in `core/model.py`.

   In order to make sense of the predicted class digits, we will add the `CLASS_DIGIT_TO_LABEL` variable to the `config.py` file. This will serve as a mapping between class digits and labels to make the output more understandable to the user. 


    ```python
    CLASS_DIGIT_TO_LABEL = {
      0: "T-shirt/top",
      1: "Trouser",
      2: "Pullover",
      3: "Dress",
      4: "Coat",
      5: "Sandal",
      6: "Shirt",
      7: "Sneaker",
      8: "Bag",
      9: "Ankle boot"
    }
    ```

    We will import this map at the top of the `core/model.py` file.

    ```python
    from config import DEFAULT_MODEL_PATH, CLASS_DIGIT_TO_LABEL
    ```

    The class with the highest probability will be assigned to the input image. Here, we will use our imported `CLASS_DIGIT_TO_LABEL` variable to map the class digit to the corresponding label.

    Add the below code under the `_post_process` method in `core/model.py`.
    
    _NOTE_: Remove `return result` and add the below code.
    
    ```python
    # Extract prediction probability using `amax` and
    # digit prediction using `argmax`
    return [{'probability': np.amax(result),
            'prediction': CLASS_DIGIT_TO_LABEL[np.argmax(result)]}]
    ```
   
6. Finally, assign the output from the post-processing step to the appropriate response field in `api/predict.py` to link the processed model output to the API.

   Replace the original code:
   
   ```python
   label_preds = [{'label_id': p[0], 'label': p[1], 'probability': p[2]} for p in [x for x in preds]]
   result['predictions'] = label_preds
   ```
   
   with
   
   ```python
   result['predictions'] = preds
   ```

## Build the model Docker image

_NOTE_: Docker app needs to be running to complete the below steps

If you're using your own file, please generate the md5 checksum for your own model file, and replace it with the value on the left. If you want to skip this step, feel free to remove the entire RUN-statement from the Dockerfile.

To build the docker image locally, run:

```
$ docker build -t max-fashion-mnist .
```

`-t` option is used to tag the docker image. Here, we are tagging the docker image with the name `max-fashion-mnist`.

If you want to print debugging messages make sure to set `DEBUG=True` in `config.py`.

## Run the model server

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 max-fashion-mnist
```

Test the microservice using the image [here](https://github.com/CODAIT/presentations/blob/master/workshops/2019-10-29_ODSC-WEST/max-fashion-mnist-wrapping-solution/samples/1.jpeg).

## (Optional) Update Test Script

1. Add test images to the `samples/` directory. In our implementation, we have added a picture of the `T-shirt/top` category and named it `1.jpeg`.

2. Add a few integration tests using pytest in tests/test.py to verify that your model works. 

   Example:

   - Update model endpoint and sample input file path.

      ```python
      model_endpoint = 'http://localhost:5000/model/predict'
      file_path = 'samples/1.jpeg'

      with open(file_path, 'rb') as file:
        file_form = {'file': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
      ```

   - Check if the prediction is `T-shirt/top`.

      ```python
      assert response['predictions'][0]['prediction'] == "T-shirt/top"
      ```

3. To enable Travis CI testing uncomment the docker commands and pytest command in `.travis.yml`.


## Resources

1. IBM Developer - [Model Asset Exchange](https://ibm.biz/model-exchange)

2. IBM Developer - [Data Asset Exchange](https://ibm.biz/data-exchange)

3. Model Asset Exchange - [Learning Path](https://ibm.biz/max-learning-path)

4. Model Asset Exchange - [Model Status](https://ibm.biz/max-status)

5. Model Asset Exchange [Framework](https://ibm.biz/max-framework)

6. Model Asset Exchange - [NodeRed](https://ibm.biz/max-node-red)
