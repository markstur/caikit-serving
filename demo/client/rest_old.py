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

# Standard
from os import path, getenv
import json
import sys

# Third Party
import grpc
import requests

# Local
from caikit.config.config import get_config
from caikit.runtime.service_factory import ServicePackageFactory
import caikit

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory
from grpc_reflection. v1alpha.proto_reflection_descriptor_database import (
    ProtoReflectionDescriptorDatabase,
)

if __name__ == "__main__":
    # Add the runtime/library to the path
    sys.path.append(
        path.abspath(path.join(path.dirname(__file__), "../../"))
    )

    # Load configuration for Caikit runtime
    CONFIG_PATH = path.realpath(
        path.join(path.dirname(__file__), "config.yml")
    )
    caikit.configure(CONFIG_PATH)

    inference_service = ServicePackageFactory().get_service_package(
        ServicePackageFactory.ServiceType.INFERENCE,
    )

    model_id = "sentence-transformers/mini"

    top_k = 2
    queries = ["first sentence", "any sentence"]
    print("QUERIES: ", queries)

    host = getenv('CAIKIT_EMBEDDINGS_HOST') if getenv('CAIKIT_EMBEDDINGS_HOST') else 'localhost'
    # grpc deleted

    if get_config().runtime.http.enabled:
        # REST payload
        payload = {
                "inputs": queries
        }
        response = requests.post(
            f"http://{host}:8080/api/v1/{model_id}/task/embedding-retrieval",
            json=payload,
            timeout=1,
        )

        print("RESPONSE: ", response)

        print("===================")
        print("RESPONSE from HTTP:")
        print(json.dumps(response.json(), indent=4))
