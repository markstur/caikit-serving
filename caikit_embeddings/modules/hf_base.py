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

# Third Party
from transformers import AutoModel, AutoTokenizer

# Local
from caikit.core import ModuleConfig

DEFAULT_MODEL = None
DEFAULT_MODEL_REVISION = None


class HFBase:
    def __init__(self, model=None, tokenizer=None) -> None:
        """This function gets called by `.load` and `.train` function
        which initializes this module.
        """
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer

    @classmethod
    def read_config(cls, model_name_or_path, default_model, default_model_revision):
        config = ModuleConfig.load(model_name_or_path)
        model_name = config.get("hf_model", default_model)
        model_revision = config.get("hf_model_revision", default_model_revision)
        return model_name, model_revision

    @classmethod
    def load(cls, model_config_path: str):
        model_name, model_revision = cls.read_config(
            model_config_path, DEFAULT_MODEL, DEFAULT_MODEL_REVISION
        )
        return cls.bootstrap(model_name, revision=model_revision)

    @classmethod
    def bootstrap(cls, pretrained_model_name_or_path: str, revision=None):
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path, revision=revision
        )
        model = AutoModel.from_pretrained(
            pretrained_model_name_or_path, revision=revision
        )
        return cls(model, tokenizer)
