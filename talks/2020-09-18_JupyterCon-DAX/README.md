# JupyterCon 2020
## Introduction to Elyra: AI-centric extensions to JupyterLab

September 18th, 2020

- Slides: [slides](https://github.com/CODAIT/presentations/tree/master/talks/2020-09-18_JupyterCon-DAX)

- Elyra Github: [Elyra 1.1.0](https://github.com/elyra-ai/elyra)

- Data Asset Exchange: [http://ibm.biz/data-exchange](http://ibm.biz/data-exchange)

- Elyra demo Github: [JFK Weather](https://github.com/elyra-ai/examples/tree/master/pipelines/dax_noaa_weather_data)

- Model Asset Exchange: [http://ibm.biz/model-exchange](http://ibm.biz/model-exchange)

Ways to run pipelines:

- Try JupyterLab and Elyra on pre-built docker image:
The command below starts a clean Elyra environment:

```
docker run -it -p 8888:8888 elyra/elyra:1.1.0 jupyter lab --debug
```

To make a local directory containing your Notebooks (e.g. ${HOME}/opensource/jupyter-notebooks/) available in your
docker container, you can use a mount command similar to the following:

```
docker run -it -p 8888:8888 -v ${HOME}/opensource/jupyter-notebooks/:/home/jovyan/work -w /home/jovyan/work elyra/elyra:1.1.0 jupyter lab --debug
```

- Or you can use Binder: https://mybinder.org/v2/gh/elyra-ai/elyra/v1.0.0?urlpath=lab/tree/binder-demo

- Or you can install Elyra: https://github.com/elyra-ai/elyra#installation