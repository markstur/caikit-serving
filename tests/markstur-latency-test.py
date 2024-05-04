# Third Party
import grpc
from os import path
import sys
import os
import timeit
import numpy as np
import csv

# Local
import caikit
from caikit.runtime.service_factory import ServicePackageFactory

# Add the runtime/library to the path
sys.path.append(
    path.abspath(path.join(path.dirname(__file__), "../demo/client"))
)

# Load configuration for Caikit runtime
CONFIG_PATH = os.getenv("CONFIG_PATH")
caikit.configure(CONFIG_PATH)

# NOTE: The model id needs to be a path to folder.
# NOTE: This is relative path to the models directory
MODEL_ID = os.getenv("MODEL", "sentence-transformers/all-minilm-l6-v2")

inference_service = ServicePackageFactory().get_service_package(
    ServicePackageFactory.ServiceType.INFERENCE,
)

port = os.getenv('CAIKIT_EMBEDDINGS_PORT') if os.getenv('CAIKIT_EMBEDDINGS_PORT') else 8085
host = os.getenv('CAIKIT_EMBEDDINGS_HOST') if os.getenv('CAIKIT_EMBEDDINGS_HOST') else 'localhost'

# mTLS is required through the router, insecure for direct testing against model
if (os.getenv('CAIKIT_EMBEDDINGS_CACERT')):
    ca_cert_file = os.getenv('CAIKIT_EMBEDDINGS_CACERT')
    cert_file = os.getenv('CAIKIT_EMBEDDINGS_CERT')
    key_file = os.getenv('CAIKIT_EMBEDDINGS_KEY')
    root_cert = open(ca_cert_file).read().encode()
    cert = open(cert_file).read().encode()
    key = open(key_file).read().encode()
    credentials = grpc.ssl_channel_credentials(root_cert, key, cert)
    channel = grpc.secure_channel(host + ':' + str(port), credentials)
else:
    channel = grpc.insecure_channel(f"{host}:{port}")

client_stub = inference_service.stub_class(channel)

# Test control parameter
ITERATIONS = 5
PRINT_RESPONSE = True
MAX_NEW_TOKENS = 248
INITIAL_WARMUP_CYCLES = int(os.environ.get('INITIAL_WARMUP_CYCLES') or '5')

latList = []

X_TEXT = 75
X_DATASET = 10

texts = [
    "test first sentence " * X_TEXT,
    "another test sentence " * X_TEXT,
]

texts_dataset = []
for x in range(X_DATASET):
    texts_dataset.extend(texts)

# texts_dataset = []
# Load dataset from tsv file
# with open(os.getenv('DATASET')) as f:
    # tsv_file = csv.reader(f, delimiter="\t")
    # for line in tsv_file:
        # text = line[1]
        # print(text)
        # texts_dataset.append(text)


if __name__ == '__main__':
    print(f"Targeting host: {host + ':' + str(port)}...")

    tik = timeit.default_timer()
    print(f"Starting warmup with {INITIAL_WARMUP_CYCLES} cycles...")
    # INITIAL_WARMUP_CYCLES
    for i in range(INITIAL_WARMUP_CYCLES):
        request = inference_service.messages.EmbeddingTasksRequest(texts=texts)
        # Fetch predictions from server (infer)
        response = client_stub.EmbeddingTasksPredict(
            request, metadata=[("mm-model-id", MODEL_ID)]
        )
        # Print response
        print("INPUTS TEXTS: ", texts)
<<<<<<< Updated upstream
        print("response: ", response.results)
=======
        print("RESULTS: [")
        for d in response.results.vectors:
            woo = d.WhichOneof("data")  # which one of data_<float_type>s did we get?
            print(getattr(d, woo).values)
        print("]")
        print("LENGTH: ", len(response.results.vectors), " x ", len(getattr(response.results.vectors[0], woo).values))
>>>>>>> Stashed changes
    tok = timeit.default_timer()

    print(f"Warmup terminated in {tok-tik} sec.")

    # Start latency test 
    start_time = timeit.default_timer()
    for i in range(ITERATIONS):
        s = timeit.default_timer()
        request = inference_service.messages.EmbeddingTasksRequest(
            texts=texts_dataset  # , truncate_input_tokens=-1
        )
        # Fetch predictions from server (infer)
        response = client_stub.EmbeddingTasksPredict(
            request, metadata=[("mm-model-id", MODEL_ID)]
        )
<<<<<<< Updated upstream
        # Print response - comment out for real testing...
        #print("INPUTS TEXTS: ", texts_dataset)
        #print("response: ", response.results)
=======
        # Print response
        # print("INPUTS TEXTS: ", texts_dataset)
        # print("RESULTS: [")
        for d in response.results.vectors:
            woo = d.WhichOneof("data")  # which one of data_<float_type>s did we get?
            _ = getattr(d, woo).values
>>>>>>> Stashed changes
        latList.append(timeit.default_timer() - s)
    elapsed = timeit.default_timer() - start_time

    # if PRINT_RESPONSE:
        # print(response)
    lat= np.array(latList)
    print('**** LATENCY TEST REPORT for ' + MODEL_ID + ' at ' + host +  ' ****')
    print("Iterations: ", ITERATIONS)
    print("Min Latency:", round(np.min(lat),2), ' Sec')
    print("Max Latency:", round(np.max(lat),2), ' Sec')
    print("25 Percentile:", round(np.percentile(lat, 25),2), ' Sec')
    print("50 Percentile:", round(np.percentile(lat, 50),2), ' Sec')
    print("75 Percentile:", round(np.percentile(lat, 75),2), ' Sec')
    print("90 Percentile:", round(np.percentile(lat, 90),2), ' Sec')
    print("99 Percentile:", round(np.percentile(lat, 99),2), ' Sec')
    print("Average Latency:", round(np.average(lat),2), ' Sec')
