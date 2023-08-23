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

import alog
from caikit.core import ModuleBase, ModuleLoader, ModuleSaver, module
from caikit.core.toolkit.errors import error_handler
from caikit_template.modules.embedding_retrieval import EmbeddingRetrievalTask
from caikit_template.data_model.embedding_vectors import EmbeddingResult

import os

logger = alog.use_channel("<SMPL_BLK>")
error = error_handler.get(logger)


@module(
    "00110203-0405-0607-0809-0a0b02dd0e0f",
    "HelloWorldModule",
    "0.0.1",
    EmbeddingRetrievalTask,
)
class HelloWorldModule(ModuleBase):

    def __init__(self, model=None) -> None:
        """Function to initialize the HelloWorld.
        This function gets called by `.load` and `.train` function
        which initializes this module.
        """
        super().__init__()
        self.model = model

    @classmethod
    def load(cls, model_path: str, **kwargs):
        """Load a caikit model
        Args:
            model_path: str
                Path to caikit model.
        """
        loader = ModuleLoader(model_path)
        config = loader.config

        # Utilize config to access parameters needed.
        # For example, if you need to extract tokenizer path, you can do:
        # config.tokenizer_path
        # You can do a type check on it, using:
        # error.type_check("<TMP94715366E>", str, tokenizer_path=config.tokenizer_path)

        # Load model artifact
        model = None  # replace this with model load code such as `torch.load`
        return cls(model)

    def run(self, text: str) -> EmbeddingResult:
        """Run inference on model.
        Args:
            text: str
                Input text to be processed
        Returns:
            EmbeddingResult: the output
        """
        # This is the main function used for inferencing.
        # NOTE:
        # 1. Output of a run function needs to be a data model. In this case
        #    we have used HelloWorldPrediction as an example.
        # 2. The input and output data model (for example HelloWorldPrediction for output)
        #    are only used for demo purposes. A developer of a new module
        #    can use any data model (as output). There are a lot of 
        #    pre-built (https://github.com/caikit/caikit/tree/main/caikit/interfaces)
        #    data models provided already, but if those are not suitable for the use-case,
        #    then one can choose to build their own data model as well.
        # 3. It is required for the `run` function to have proper doc strings and type hints 
        #    as these get used for runtime automation
        # 4. This function is meant to process single example inference only.
        #    For a batch request, please implement `run_batch` function, which would
        #    accept list of text (as example) as input and return List of
        #    `HelloWorldPrediction` (as an example) as output.
        return EmbeddingResult([1.23, 2.34])
        # this works too! return EmbeddingResult([[1.23], [2.34]])

    def save(self, model_path, *args, **kwargs):
        """Function to save model in caikit format.
        This will generate store models on disk in a folder, which would be directly
        consumable by caikit.runtime framework.

        Args:
            model_path: str
                Path to store model into
        """
        module_saver = ModuleSaver(
            self,
            model_path=model_path,
        )
        with module_saver:

            temp_model_file = os.path.join(model_path,  "temp_model.txt")
            # Write into temp_model_file as example
            with open(temp_model_file, "w") as f:
                for idx in range(3):
                    f.write(str(idx))

            config_options = {
                "tokenizer_path": "<EXAMPLE>",
                "temp_model_path": temp_model_file
            }
            module_saver.update_config(config_options)

    @classmethod
    def bootstrap(cls, pretrained_model_path):
        """Optional: Function that allows to load a non-caikit model artifact
        such as open source models from TF hub or HF and load them into
        this module.
        """
        # Replace following with model load code such as `transformers.from_pretrained`
        model = None
        return cls(model)
