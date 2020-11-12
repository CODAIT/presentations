# PyCon Sweden 2020
## Introduction to Elyra: AI-centric extensions to JupyterLab

November 12th, 2020

- Slides: [slides](https://github.com/CODAIT/presentations/tree/master/talks/2020-11-12_PyCon-DAX)

- Elyra Github: [Elyra 1.4.0](https://github.com/elyra-ai/elyra)

- Data Asset Exchange: [http://ibm.biz/data-exchange](http://ibm.biz/data-exchange)

- Elyra demo Github: [JFK Weather](https://github.com/elyra-ai/examples/tree/master/pipelines/dax_noaa_weather_data)

- Model Asset Exchange: [http://ibm.biz/model-exchange](http://ibm.biz/model-exchange)

## Try Elyra

### Install Elyra: 

See Elyra Github page: https://github.com/elyra-ai/elyra#installation

### Use Binder: 

You can try out some of Elyra features using the [My Binder](https://mybinder.readthedocs.io/en/latest/) service.
Click on a link below to try Elyra, on a sandbox environment, without having to install anything.

- [![Launch latest stable version](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/elyra-ai/elyra/v1.3.3?urlpath=lab/tree/binder-demo) (Latest stable version - see [changelog](/docs/source/getting_started/changelog.md) for recent updates)
- [![Launch latest development version](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/elyra-ai/elyra/master?urlpath=lab/tree/binder-demo) (Development version - expect longer image load time due to just-in-time build)

### Use Docker: 

The command below starts the most recent development build in a clean environment:

```
docker run -it -p 8888:8888 elyra/elyra:dev jupyter lab --debug
```
For more information, visit [Elyra Github](https://github.com/elyra-ai/elyra) page.
