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
import numpy as np
import sys
import os

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
MODEL_ID = os.getenv("MODEL", "sentence-transformers/mini")

inference_service = ServicePackageFactory().get_service_package(
    ServicePackageFactory.ServiceType.INFERENCE,
)

port = os.getenv('CAIKIT_EMBEDDINGS_PORT') if os.getenv('CAIKIT_EMBEDDINGS_PORT') else 8085
host = os.getenv('CAIKIT_EMBEDDINGS_HOST') if os.getenv('CAIKIT_EMBEDDINGS_HOST') else 'localhost'
channel = grpc.insecure_channel(f"{host}:{port}")
client_stub = inference_service.stub_class(channel)

# Create request object

text257 = (
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10 100
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10 100
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10 100
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10 100
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10
    "x x x x x "  # counting spaces 10 100
    "y y w y"  # 256? -- NOT COUNTING SPACES
    " z"  # 257 BOOM!!!
)

text256 = text257[:-2]  # space z
text255 = text256[:-2]  # space y
text254 = text255[:-2]  # space w

text300 = (
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    # "test first sentence with ten"
)

text1000 = (
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"
    "test first sentence with ten tokens seven eight nine ten"  # 100
)

text257plus = text257 + " a b c d e f g h i j "+  text257
text257plusplus = text257 + " a b c d e f g h i j " + text300 + text300
results = []
truncate_input_tokens = 255 # -1   # 260
for text in [text257plus, text257plusplus]:
    request = inference_service.messages.EmbeddingTaskRequest(text=text, truncate_input_tokens=truncate_input_tokens)

    # Fetch predictions from server (infer)
    response = client_stub.EmbeddingTaskPredict(
        request, metadata=[("mm-model-id", MODEL_ID)]
    )

    # Print response
    print("response=", response)

    print("INPUTS TEXTS: ", text)
    print("RESULT: ")
    d = response.result
    woo = d.WhichOneof("data")  # which one of data_<float_type>s did we get?
    vals = getattr(d, woo).values
    print(vals)
    print("")
    print("LENGTH: ", "1", " x ",
    len(vals))
    results.append(vals)

print("COMPARE: ", results)
assert np.allclose(results[0], results[1])
assert results[0] ==  results[1]
assert np.allclose(results[0], results[1])


