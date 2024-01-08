# Caikit Embeddings Deployment
This readme will describe how to deploy a given Embeddings model. Optionally, you can also deploy  a gRPC UI endpoint for development purposes. This document assumes the Embeddings Router has already been installed.


### Set the Image Pull secret

Copy credentials obtained from the container registry owner into environment variable
```bash
export ICR_APIKEY=<icr-credential>
```
Copy credential into secret and link to default service account
```bash
oc create secret docker-registry icr-caikit-image \
  --docker-server=icr.io --docker-username=iamapikey \
  --docker-password=${ICR_APIKEY} --docker-email=iamapikey
oc secrets link serviceaccount/default secrets/ icr-caikit-image --for=pull
```

### Add components to Helm repo
Install helm our your workstation, then run the following:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami 
helm repo update
helm dependency update
```

## Deploy the Service

1. From your workstation, log into your OCP cluster and desired project or create new one.  Obtain the COS credentials needed to access the model you are deploying. 
 
2.  Then install your model's helm chart by running the following script:
```bash
cd charts
../assets/deploy-devstage.sh {namespace} {model id} {access key} {secret key}    
# The above assumes the model values file was already created.  If you're on-boarding a new model, see below.
# There are 4 arguments to shell: namespace, model-id (by convention, model-id should ALWAYS be lower-cased), cos access and secret keys
# There are comments within the deploy scripts located at .../deployment/assets
``` 

## Conditional GPU Allocation

The code for enabling GPU resource usage for sentence-transformers already handles the cuda/cpu selection automatically [SentenceTransformer.py](https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/SentenceTransformer.py#L104). However, the following configuration needs to be added to a models values file if a GPU  is desired:

```yaml
  resources:
    limits:
      nvidia.com/gpu: "1"
```
Under `spec > spec > container > resources`, the above lines provide the GPU availability in cluster to be allocated.

## Enabling the gRPC UI for the service
If the gRPC UI is desired, deploy it as follows:
1. Create the deployment by utilizing the cluster specific yaml file located at .../deployment/deployment-files.

```bash
oc apply -f deployment-caikit-emb-grpc-ui-{cluster}.yaml
# Note this endpoint assumes the slate model was deployed and sends requests to it.
```
This will create the deployment, service and route to access the gRPC at the browser. 

Opening the route created, you should be able to see this view:
![grpc_ui](./assets/grpc-ui.png)


### TLS enablement
The embeddings router is TLS enabled.  
But if the router is NOT used for a given scenario (not typical), and the model server itself needs to be TLS enabled, check the documentation at [deployment/tls-enablement](./tls-enablement/README.md).


## Onboarding models

- The `demo/models` folder is now a PVC mounted, that points to a bucket named `caikit-embeddings-models-config`;
> PVC yaml can be found at [pvc-models.yaml](pvc-models.yaml)
- Each user of the service can upload the models they wish to use, as long as they follow the same structure as before.
- See the image bellow to check how the bucket structure convention must be:
  
<center>
    <img src="./assets/dir.png">
</center>

- Under the `model-full-name` dir there must be `artifacts` to where the `MODELS_LIST` will be pointed to, and `config.yaml` file in which the key `artifacts_path` must also point to the `artifacts` folder of the model.
- You must now create a helm values file for the new model in order to deploy it.  The values files are located at: .../deployment/charts.
- The name of the values file must follow the convention: {model id}-values.yaml 
- Use prior values files as examples when building out your new file.

## Configuring the Embeddings router for each onboarded model
The config map named "fmaas-embeddings-router" must be updated when a new embeddings model is added.  
The key/value pairing to add is a simple mapping of the new model id to its service endpoint:  
{model id}:{service-name}:8085  

For example:  
```bash
ibm/slate.30m.english.rtrvr-26.10.2023: caikit-embeddings-ibm-slate-30m-english-rtrvr:8085
```