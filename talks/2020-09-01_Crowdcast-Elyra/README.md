# CrowdCast IBM Developer

September 1st, 2020 | 9:30am-10:30am (PT)

Register or Replay [here](https://www.crowdcast.io/e/introduction-to-elyra-ai/register?utm_source=profile&utm_medium=profile_web&utm_campaign=profile).

- Slides: [Talk Slides](https://github.com/CODAIT/presentations/tree/master/talks/2020-09-01_Crowdcast-Elyra)

- Elyra Github: [Latest Elyra](https://github.com/elyra-ai/elyra)

- Elyra demo Github: [Elyra Examples](https://github.com/elyra-ai/examples/)

- Elyra Tutorials: [KubeFlow Executions](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world)

Ways to run pipelines:

- Try JupyterLab and Elyra on pre-built docker image:
The command below starts the latest Elyra release in a clean environment:

```
docker run -it -p 8888:8888 elyra/elyra:latest jupyter lab --debug
```

To make a local directory containing your Notebooks (e.g. ${HOME}/opensource/jupyter-notebooks/) available in your
docker container, you can use a mount command similar to the following:

```
docker run -it -p 8888:8888 -v ${HOME}/opensource/jupyter-notebooks/:/home/jovyan/work -w /home/jovyan/work elyra/elyra:latest jupyter lab --debug
```

- Or you can use Binder: https://mybinder.org/v2/gh/elyra-ai/elyra/v1.1.0?urlpath=lab/tree/binder-demo

- Or you can install Elyra: https://elyra.readthedocs.io/en/latest/getting_started/installation.html#

## Resources:

- Data Asset eXchange: [http://ibm.biz/data-exchange](http://ibm.biz/data-exchange)

- Model Asset eXchange: [http://ibm.biz/model-exchange](http://ibm.biz/model-exchange)
