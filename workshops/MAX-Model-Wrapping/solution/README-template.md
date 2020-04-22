[![Build Status](https://travis-ci.com/IBM/[MODEL REPO NAME].svg?branch=master)](https://travis-ci.com/IBM/[MODEL REPO NAME]) [![Website Status](https://img.shields.io/website/http/[MODEL DOCKER TAG].max.us-south.containers.appdomain.cloud/swagger.json.svg?label=api+demo)](http://[MODEL DOCKER TAG].max.us-south.containers.appdomain.cloud/)

[<img src="docs/deploy-max-to-ibm-cloud-with-kubernetes-button.png" width="400px">](http://ibm.biz/max-to-ibm-cloud-tutorial)

# IBM Developer Model Asset Exchange: [MODEL NAME]

> This file contains the README template for a new model for Model Asset Exchange.
Refer to other published MAX models for examples of how the README components are completed.
Most sections that need to be updated are either marked in brackets or reference this skeleton repo.
Some helpful hints are also included in comment blocks like this one. Please remember to delete the 
comment blocks before publishing.

> Don't forget to update `samples/README.md` as well.

This repository contains code to instantiate and deploy a [MODEL NAME].
[ADD A DESCRIPTION OF THE MODEL HERE - see other MAX models for examples]

The model is based on the [ADD OPEN SOURCE MODEL]([LINK TO MODEL]). The model files are hosted on
[IBM Cloud Object Storage]([LINK TO SPECIFIC SOFTLAYER LOCATION]).
The code in this repository deploys the model as a web service in a Docker container. This repository was developed
as part of the [IBM Developer Model Asset Exchange](https://developer.ibm.com/exchanges/models/) and the public API is powered by [IBM Cloud](https://ibm.biz/Bdz2XM).

## Model Metadata
| Domain | Application | Industry  | Framework | Training Data | Input Data Format |
| ------------- | --------  | -------- | --------- | --------- | -------------- | 
| [INSERT DOMAIN] | [INSERT APPLICATION] | [INSERT INDUSTRY] | [INSERT FRAMEWORK] | [INSERT TRAINING DATA] | [INSERT INPUT DATA FORMAT] |

## Benchmark

The predictive performance of the model can be characterized by the benchmark table below.

_Note: The performance of a model is not the only significant metric. The level of bias and fairness incorporated in the model are also of high importance. Learn more by reading up on the [AI Fairness 360 open source toolkit](http://ibm.biz/AI_Fairness_360)._



|  | [DATASET 1] | [DATASET 2]   | [DATASET 3]  |
| -------- | --------  | -------- | --------- |
| [METRIC 1] | [VALUE] | [VALUE] | [VALUE] |
| [METRIC 2] | [VALUE] | [VALUE] | [VALUE] |

## References

> This section should include links to relevant papers, github repos and dataset home pages. Please follow the standard format for references.

* _[AUTHOR 1, AUTHOR 2]_, ["PAPER NAME"]([LINK TO PAPER]), [JOURNAL / SITE], [YEAR].
* [GITHUB REPO]([LINK TO REPO])

## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Model Weights | [LINK TO LICENSE] | [LINK TO LICENSE IN SOURCE] |
| Model Code (3rd party) | [LINK TO LICENSE] | [LINK TO LICENSE IN SOURCE] |
| Test samples | [LINK TO LICENSE] | [samples README](samples/README.md) |

## Pre-requisites:

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the [installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is [SET NECESSARY GB] Memory and [SET NECESSARY CPUs] CPUs.

# Deployment options

* [Deploy from Docker Hub](#deploy-from-docker-hub)
* [Deploy on Red Hat OpenShift](#deploy-on-red-hat-openshift)
* [Deploy on Kubernetes](#deploy-on-kubernetes)
* [Run Locally](#run-locally)

## Deploy from Docker Hub

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 codait/[MODEL DOCKER TAG]
```

This will pull a pre-built image from Docker Hub (or use an existing image if already cached locally) and run it.
If you'd rather checkout and build the model locally you can follow the [run locally](#run-locally) steps below.

## Deploy on Red Hat OpenShift

You can deploy the model-serving microservice on Red Hat OpenShift by following the instructions for the OpenShift web console or the OpenShift Container Platform CLI [in this tutorial](https://developer.ibm.com/tutorials/deploy-a-model-asset-exchange-microservice-on-red-hat-openshift/), specifying `codait/[MODEL DOCKER TAG]` as the image name.

## Deploy on Kubernetes

You can also deploy the model on Kubernetes using the latest docker image on Docker Hub.

On your Kubernetes cluster, run the following commands:

```
$ kubectl apply -f https://github.ibm.com/CODAIT/[MODEL REPO NAME]/raw/master/[MODEL DOCKER TAG].yaml
```

The model will be available internally at port `5000`, but can also be accessed externally through the `NodePort`.

A more elaborate tutorial on how to deploy this MAX model to production on [IBM Cloud](https://ibm.biz/Bdz2XM) can be found [here](http://ibm.biz/max-to-ibm-cloud-tutorial).

## Run Locally

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Development](#4-development)
5. [Cleanup](#5-cleanup)


### 1. Build the Model

Clone this repository locally. In a terminal, run the following command:

```
$ git clone https://github.ibm.com/CODAIT/[MODEL REPO NAME].git
```

Change directory into the repository base folder:

```
$ cd [MODEL REPO NAME]
```

To build the docker image locally, run: 

```
$ docker build -t [MODEL DOCKER TAG] .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU only (we will add support for GPU images later).


### 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 [MODEL DOCKER TAG]
```

### 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load it. From there you can explore the API and also create test requests.

[INSERT DESCRIPTION OF HOW TO USE MODEL ENDPOINT]

> Example description for image upload models: Use the `model/predict` endpoint to load a test image (you can use one of the test images from the `samples` folder) and get predicted labels for the image from the API.

![INSERT SWAGGER UI SCREENSHOT HERE](docs/swagger-screenshot.png)

You can also test it on the command line, for example:

```
$ curl -F "image=@samples/[SAMPLE IMAGE]" -XPOST http://localhost:5000/model/predict
```

You should see a JSON response like that below:

```json
{
  "status": "ok",
  "predictions": [
      ["INSERT EXAMPLE OUTPUT"]
  ]
}
```

### 4. Development

> Please remember to set `DEBUG = False` when publishing the model. 

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will then need to rebuild the docker image (see [step 1](#1-build-the-model)).

### 5. Cleanup

To stop the Docker container, type `CTRL` + `C` in your terminal.

## Train this Model on Watson Machine Learning

> Remove this section if this model cannot be trained using custom data. Refer to https://github.ibm.com/CODAIT/max-model-training for details on how to enable a model for custom training.

This model supports both fine-tuning with transfer learning and training from scratch on a custom dataset. Please follow the steps listed under the [training readme](training/README.md) to retrain the model on [Watson Machine Learning](https://www.ibm.com/cloud/machine-learning), a deep learning as a service offering of [IBM Cloud](https://ibm.biz/Bdz2XM).
