# Deploy to production with Kubernetes

## Requirements
- Docker
- a Docker image
- an [IBM Cloud account](https://ibm.biz/BdzAHm)
- the [IBM Cloud command-line tools](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started), including `kubectl`
- (recommended) basic knowledge on Kubernetes (e.g. [this blogpost](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16))

## Instructions

### 1. Log in to IBM Cloud and create a (free) Kubernetes cluster
   
Find the [cluster in the catalog](https://cloud.ibm.com/kubernetes/catalog/cluster) and follow the steps to create a Kubernetes cluster.

### 2. Access the Kubernetes cluster
   
Following the creation of the cluster, it takes a couple minutes for the cluster to finalize setting up. Use this time to set up the `ibmcloud` CLI to access the cluster. Instructions, including how to download and install the CLI, are found in the `Access` tab of the dashboard.

The instructions include:

- Logging in to the cluster using the CLI
- Downloading the kubeconfig files for your cluster
- Setting the KUBECONFIG environment variable

### 3. Upload your Docker image to DockerHub
   
Your Kubernetes cluster will need to download the container image of your model in order to run it. Log in to [DockerHub](https://hub.docker.com/) and upload the image to your account.

The link to your image will have the following format:

`[account-username]/[image-name]:[version-tag]`

If you have your image built locally, you can upload it using the Docker command line tools.

```bash
docker login
```
```bash
docker push [account-username]/[image-name]:[version-tag]
```

Replace the `[account-username]` with your Docker username, `[image-name]` with the name of the image you built, and `[version-tag]` with how you want to label the current version of the image (e.g. `v1`).

### 4. Deploy

Spinning up our application is typically accomplished in two steps.
- Create a Service
- Create a Deployment

Every step in the configuration of the cluster is achieved by applying a configuration file (also called `configmap`) to the cluster. These configmaps are formatted in the YAML markup language, for which templates are abundantly present online. We can design  separate YAML files for every aspect of the deployment, or we can stitch them together in one complete YAML file, such as the `max-skeleton.yaml` file.

- Service

    ```yaml
    # Define a service
    apiVersion: v1
    kind: Service
    metadata:
    name: max-skeleton
    spec:
    selector:
        app: max-skeleton
    ports:
    - port: 5000
    type: NodePort
    ```

- Deployment

    ```yaml
    # Define a deployment
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
    name: max-skeleton
    labels:
        app: max-skeleton
    spec:
    selector:
        matchLabels:
        app: max-skeleton
    replicas: 1
    template:
        metadata:
        labels:
            app: max-skeleton
        spec:
        containers:
        - name: max-skeleton
            image: codait/max-skeleton:latest
            ports:
            - containerPort: 5000
    ```

These two components have been stitched together into one file (`max-skeleton.yaml` in this repository).
Replace the `max-skeleton` placeholder with the name you choose to give your application and model. In addition, replace `codait/max-skeleton:latest` with the location of your docker image on Dockerhub. The format is `[account-username]/[image-name]:[version-tag]`. Save the file, and use the `kubectl` CLI to configure this map.

```bash
kubectl create -f max-skeleton.yaml
```

(optional) Use the following commands to do a couple status checks. Your deployment should be up and running.

```bash
# show services
kubectl get services
# show deployments
kubectl get deployment [MODEL-NAME]
# show nodes
kubectl get nodes -o wide
```

_NOTE: This is a template configuration. Once you get comfortable with spinning up containers on Kubernetes, you will need to adjust the configmap for your specific use-case._

### 5. Access your application

- Note down the external IP address of your node (value for `EXTERNAL-IP`)

    ```bash
    kubectl get nodes -o wide
    ```

- Note down the exposed port (the number under `PORT(S)` in the `30000-32767` range)

    ```bash
    kubectl get svc
    ```

Now, combine these two into the following format:

`http://[EXTERNAL-IP]:[PORT-NUMBER]`

Navigate there and you should see the API of your application. Congratulations!

_To learn more about scaling this cluster and advanced configuration such as LoadBalancers or Ingress, feel free to ask us about more advanced resources._

## More deployment-related resources

- [Deploy MAX models to IBM Cloud with Kubernetes](https://developer.ibm.com/tutorials/deploy-max-models-to-ibm-cloud-with-kubernetes/)
- [Kubernetes 101 Medium blogpost](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16)
- [Linode.com container deployment tutorial](https://www.linode.com/docs/applications/containers/kubernetes/deploy-container-image-to-kubernetes/)
