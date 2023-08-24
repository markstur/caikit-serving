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

# Local
import caikit
from caikit.runtime.service_factory import ServicePackageFactory

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
MODEL_ID = "mini"

inference_service = ServicePackageFactory().get_service_package(
    ServicePackageFactory.ServiceType.INFERENCE,
)

port = 8085
channel = grpc.insecure_channel(f"localhost:{port}")
client_stub = inference_service.stub_class(channel)

# Create request object

sentences = ["test first sentence", "another test sentence"]
request = inference_service.messages.EmbeddingRetrievalTaskRequest(input=sentences)

# Fetch predictions from server (infer)
response = client_stub.EmbeddingRetrievalTaskPredict(
    request, metadata=[("mm-model-id", MODEL_ID)]
)

# Print response
print("INPUTS: ", sentences)
print("RESULTS: [")
for d in response.data:
    print("  ", d.data)
print("]")
print("LENGTH: ", len(response.data), " x ", len(response.data[0].data))
