#!/bin/bash

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data1.txt concurrency=100'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=100 \
--connections=100 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data1.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data1.txt concurrency=500'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=500 \
--connections=500 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data1.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data1.txt concurrency=800'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=800 \
--connections=800 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data1.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data1.txt concurrency=1000'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=1000 \
--connections=1000 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data1.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data1.txt concurrency=2000'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=2000 \
--connections=2000 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data1.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data50.txt concurrency=100'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=100 \
--connections=100 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data50.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443


echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data50.txt concurrency=500'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=500 \
--connections=500 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data50.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443


echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data50.txt concurrency=800'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=800 \
--connections=800 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data50.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data100.txt concurrency=100'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=100 \
--connections=100 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data100.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data100.txt concurrency=500'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=500 \
--connections=500 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data100.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443

echo 'Running with ibm/slate.30m.english.rtrvr-26.10.2023 data100.txt concurrency=800'

/tmp/perf-ghz/ghz \
--cacert /tmp/perf-ghz/ca-cert.pem \
--cert /tmp/perf-ghz/server-cert.pem \
--key /tmp/perf-ghz/server-key.pem \
--proto /tmp/perf-ghz/protos/nlpservice.proto \
--call caikit.runtime.Nlp.NlpService.EmbeddingTasksPredict \
--concurrency=800 \
--connections=800 \
--cpus=16 \
--lb-strategy='round_robin' \
--duration 30s \
--duration-stop wait \
--metadata='{"mm-model-id": "ibm/slate.30m.english.rtrvr-26.10.2023"}' \
--data-file=/tmp/perf-ghz/data100.txt \
fmaas-embeddings-fmaas-internal-embeddings.apps.fmaas-backend.fmaas.res.ibm.com:443






