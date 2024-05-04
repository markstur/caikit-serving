# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Third Party
import grpc
from os import path
import sys
import json
import os
import requests

# Local
import caikit
from caikit.runtime.service_factory import ServicePackageFactory
from caikit.config.config import get_config

# Add the runtime/library to the path
sys.path.append(
    path.abspath(path.join(path.dirname(__file__), "../../"))
)

# Load configuration for Caikit runtime
CONFIG_PATH = path.realpath(
    path.join(path.dirname(__file__), "config.yml")
)
caikit.configure(CONFIG_PATH)

# NOTE: The model id needs to be a path to folder.
# NOTE: This is relative path to the models directory
MODEL_ID = os.getenv("MODEL", "mini")

inference_service = ServicePackageFactory().get_service_package(
    ServicePackageFactory.ServiceType.INFERENCE,
)

port = os.getenv('CAIKIT_EMBEDDINGS_PORT') if os.getenv('CAIKIT_EMBEDDINGS_PORT') else 8085
host = os.getenv('CAIKIT_EMBEDDINGS_HOST') if os.getenv('CAIKIT_EMBEDDINGS_HOST') else 'localhost'
channel = grpc.insecure_channel(f"{host}:{port}")
client_stub = inference_service.stub_class(channel)

# Create request object

texts = ["test first sentence", "another test sentence"]
request = inference_service.messages.EmbeddingTasksRequest(texts=texts)

# Fetch predictions from server (infer)
response = client_stub.EmbeddingTasksPredict(
    request, metadata=[("mm-model-id", MODEL_ID)]
)

# Print response
print("INPUTS TEXTS: ", texts)
print("RESULTS: [")
for d in response.results.vectors:
    woo = d.WhichOneof("data")  # which one of data_<float_type>s did we get?
    print(getattr(d, woo).values)
print("]")
print("LENGTH: ", len(response.results.vectors), " x ",
      len(getattr(response.results.vectors[0], woo).values))

if get_config().runtime.http.enabled:
    # REST payload
    payload = {
        "inputs": ["first sentence", "any sentence"],
        "parameters": {
            "truncate_input_tokens": -1,
        },
        "model_id": MODEL_ID
    }
    response = requests.post(
        f"http://{host}:8080/api/v1/task/embedding-tasks",
        json=payload,
        timeout=1,
    )
    print("===================")
    print("RESPONSE from HTTP:")
    print(json.dumps(response.json(), indent=4))
