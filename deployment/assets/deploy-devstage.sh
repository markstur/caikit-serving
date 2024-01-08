#!/bin/bash

# Assume user is logged into OCP cluster
# Assume script is being run from ./deployment/charts directory
# A ${MODEL}-values.yaml file was created for the new model
# There are 4 arguments to shell: namespace, model-id (by convention, model-id should ALWAYS be lower-cased), cos access and secret keys
###############
# Special Note: For first time deployments into a NEW namespace ONLY. Populate and Apply 'first-time-only-templates' folder manually first (outside of helm...)
###############

NAMESPACE=$1
MODEL=$2
export COS_ACCESS_KEY=$3
export COS_SECRET_KEY=$4

MODEL=$(sed 's/\//\-/g' <<< "$MODEL")
export MODEL=$(sed 's/\./\-/g' <<< "$MODEL")
export OC_PROJECT=$NAMESPACE
export HELM_NAME=$MODEL
export FULL_NAME_OVERRIDE=caikit-embeddings-$MODEL

oc project ${OC_PROJECT}
export OC_HOST=$(oc get IngressController default -n openshift-ingress-operator -o jsonpath='{ .status.domain}')

helm dependency build
helm upgrade --install --history-max=2 -n ${OC_PROJECT} --set secrets.cosAccessKey=$COS_ACCESS_KEY,secrets.cosSecretKey=$COS_SECRET_KEY,fullnameOverride=$FULL_NAME_OVERRIDE -f ${MODEL}-values-devstage.yaml $HELM_NAME .


