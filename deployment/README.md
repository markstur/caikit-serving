# Caikit Embeddings Deployment

Deployment config for caikit embeddings.

## Deploy the Service

1. Connect to OCP cluser and desired project or create new one;

2. Create the deploymentConfig using the file at `caikit-embeddings/deployment/deploymentconfig-caikit-embeddings.yaml` - remember to point the `imagePullSecrets` name to the secrets where the icr iam key is kept.
   
3. Create the service using the file at `caikit-embeddings/deployment/service-caikit-embeddings.yaml`. Can be done through OCP UI or:
```bash
oc apply -f service-caikit-embeddings.yaml
```
4. Get the OCP host and domain through the UI or:
```sh
oc get IngressController default -n openshift-ingress-operator -o jsonpath='{ .status.domain}'
```
5. Replace the OCP host and domain in the router yaml file at `caikit-embeddings/deployment/route-caikit-embeddings.yaml`  to create the route and expose the service:
```bash
oc apply -f route-caikit-embeddings.yaml
```
6. Go to browser and access the route at `https://caikit-embeddings-route-<oc-project>.<oc-host>.<oc-domain>/docs` and you will be able to see swagger documentation for the API.

## Conditional GPU Allocation

The code for enabling GPU resource usage for sentence-transformers already handles the cuda/cpu selection automatically [SentenceTransformer.py](https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/SentenceTransformer.py#L104). However, the following configuration needs to be added to the [deploymentconfig-caikit-embeddings.yaml](./deploymentconfig-caikit-embeddings.yaml).

```yaml
  resources:
    limits:
      nvidia.com/gpu: "1"
```
Under `spec > spec > container > resources`, the above lines provide the GPU availability in cluster to be allocated.
