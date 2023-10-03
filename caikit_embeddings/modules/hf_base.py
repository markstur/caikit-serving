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
# limitations under the License

# Standard libraries
import os
from pathlib import Path

# Third Party
from sentence_transformers import SentenceTransformer

# Local
from caikit.core import ModuleConfig

DEFAULT_HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HOME = Path.home()


class HFBase:
    def __init__(self, model_config_path) -> None:
        """This function gets called by `.load` and `.train` function
        which initializes this module.
        """
        config = ModuleConfig.load(model_config_path)
        load_path = config.get("load_path")

        artifact_path = False
        if load_path:
            print("<--------------------------- load_path --------------------------->")
            print(load_path)
            if os.path.isdir(load_path):
                artifact_path = load_path
            else:
                full_path = os.path.join(model_config_path, load_path)
                if os.path.isdir(full_path):
                    artifact_path = full_path

        if not artifact_path:
            artifact_path = config.get("hf_model", DEFAULT_HF_MODEL)
            print("<--------------------------- artifact_path --------------------------->")
            print(artifact_path)

        self.model = SentenceTransformer(
            artifact_path,
            cache_folder=f"{HOME}/.cache/huggingface/sentence_transformers"
        )
