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

    model_id = "mini-rr"

    top_k = 2
    queries = ["first sentence", "any sentence"]
    documents = [
        {"document": {
            "text": "first sentence",
            "title": "first title"
        }},
        {"document": {
            "_text": "another sentence",
            "more": "more attributes here"
        }},
        {"document": {
            "nothing": "",
        }},
    ]

    print("======================")
    print("TOP K: ", top_k)
    print("QUERIES: ", queries)
    print("DOCUMENTS: ", documents)
    print("======================")

    if get_config().runtime.grpc.enabled:

        # Setup the client
        port = getenv('CAIKIT_EMBEDDINGS_PORT') if getenv('CAIKIT_EMBEDDINGS_PORT') else 8085
        host = getenv('CAIKIT_EMBEDDINGS_HOST') if getenv('CAIKIT_EMBEDDINGS_HOST') else 'localhost'
        channel = grpc.insecure_channel(f"{host}:{port}")
        client_stub = inference_service.stub_class(channel)
        reflection_db = ProtoReflectionDescriptorDatabase(channel)
        desc_pool = DescriptorPool(reflection_db)
        services = [
            x for x in reflection_db.get_services() if
            x.startswith("caikit.runtime.") and not x.endswith("TrainingService") and not x.endswith(
                "TrainingManagement")
        ]
        if len(services) != 1:
            print(f"Error: Expected 1 caikit.runtime service, but found {len(services)}.")
        service_name = services[0]
        service_prefix, _, _ = service_name.rpartition(".")
        request_name = f"{service_prefix}.RerankTaskRequest"
        request_desc = desc_pool.FindMessageTypeByName(request_name)
        rerank_docs = MessageFactory(desc_pool).GetPrototype(
            desc_pool.FindMessageTypeByName("caikit_data_model.RerankDocuments"))
        rerank_request = MessageFactory(desc_pool).GetPrototype(request_desc)

        # gRPC documents
        docs = rerank_docs(documents=documents)

        # gRPC request
        request = rerank_request(queries=queries, top_k=2)
        request = rerank_request(queries=queries, documents=docs, top_k=2)
        response = client_stub.RerankTaskPredict(
            request, metadata=[("mm-model-id", model_id)], timeout=1)

        # gRPC response
        print("RESPONSE from gRPC:")
        for i, r in enumerate(response.results):
            print("===")
            print("QUERY: ", queries[i])
            # print("RESULTS: ", r)
            for s in r.scores:
                print(f"  score: {s.score}  corpus_id: {s.corpus_id}")
                for f in s.document.items():
                    print(f"             {f[0]}: {f[1]}")

    if get_config().runtime.http.enabled:
        # REST payload
        payload = {"queries": queries, "documents": {"documents": documents}}
        payload = {
            "inputs": {
                "documents": {"documents": documents},
                "queries": queries
            },
            "parameters": {
                "top_k": 2
            }
        }
        response = requests.post(
            f"http://{host}:8080/api/v1/{model_id}/task/rerank",
            json=payload,
            timeout=1,
        )
        print("===================")
        print("RESPONSE from HTTP:")
        print(json.dumps(response.json(), indent=4))
