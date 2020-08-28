# CrowdCast IBM Developer

September 1st, 2020 | 9:30am-10:30am (PT)

Register [here](https://www.crowdcast.io/e/introduction-to-elyra-ai/register?utm_source=profile&utm_medium=profile_web&utm_campaign=profile).

- Slides: [slides](https://github.com/CODAIT/presentations/tree/master/talks/2020-09-01_Crowdcast-Elyra)

- Elyra Github: [Elyra 1.1.0](https://github.com/elyra-ai/elyra)

- Data Asset Exchange: [http://ibm.biz/data-exchange](http://ibm.biz/data-exchange)

- Elyra demo Github: [JFK Weather](https://github.com/elyra-ai/examples/tree/master/pipelines/dax_noaa_weather_data)

- Sign up for IBM Cloud: https://ibm.biz/BdqVxW

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