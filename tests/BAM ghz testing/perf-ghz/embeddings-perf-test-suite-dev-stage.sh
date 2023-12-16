#!/bin/bash

# Loop through list of models, payload files, and concurrency vectors
#
# setup - laydown the embeddings ghz files on a pod on the BAM prod cluster (endpoint is configured/hardcoded to the router in bam)
# execute as: nohup ./embeddings-perf-test-suite.sh &
# capture the output via the nohup.out file

MODELS=("ibm/slate.30m.english.rtrvr-26.10.2023" "sentence-transformers/all-minilm-l6-v2")
PAYLOADS=("data1.txt" "data50.txt" "data100.txt" "data.txt") # data.txt is original == 600
CONCURRENCY=("100" "500" "800" "1000" "2000")

for model in ${MODELS[@]}; do
  for load in ${PAYLOADS[@]}; do
    for concur in ${CONCURRENCY[@]}; do

      #Only run certain concurrency levels with given datasets...
      if [[ ${load} = "data50.txt"  && ( ${concur} = "1000" || ${concur} = "2000" ) ]]; then break ; fi
      if [[ ${load} = "data100.txt"  && ( ${concur} = "800" || ${concur} = "1000" || ${concur} = "2000" ) ]]; then break ; fi
      if [[ ${load} = "data.txt"  && ( ${concur} = "500" || ${concur} = "800" || ${concur} = "1000" || ${concur} = "2000" ) ]]; then break ; fi

      echo "Running Embeddings Performance test for ${model} with dataset: ${load} and a concurrency level=${concur}"
      /tmp/perf-ghz/ghz \
         --cacert /tmp/perf-ghz/devstage-ca-cert.pem \
         --cert /tmp/perf-ghz/devstage-server-cert.pem \
         --key /tmp/perf-ghz/devstate-server-key.pem \
         --proto /tmp/perf-ghz/protos/nlpservice.proto \
         --call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
         --concurrency=${concur} \
         --connections=${concur} \
         --timeout=180s \
         --cpus=16 \
         --lb-strategy='round_robin' \
         --duration 30s \
         --duration-stop wait \
         --metadata='{"mm-model-id": "'${model}'"}' \
         --data-file=/tmp/perf-ghz/${load} \
        fmaas-embeddings-fmaas-mig.apps.fmaas-devstage-backend.fmaas.res.ibm.com:443
    done
  done
done







