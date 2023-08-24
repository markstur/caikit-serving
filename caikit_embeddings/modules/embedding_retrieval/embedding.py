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
from caikit.core import ModuleBase, module
from caikit.core.exceptions import error_handler
from caikit_embeddings.modules.embedding_retrieval import EmbeddingRetrievalTask
from caikit_embeddings.data_model.embedding_vectors import EmbeddingResult, Vector1D

from sentence_transformers import SentenceTransformer

from ..hf_base import HFBase

from pathlib import Path
from typing import List

logger = alog.use_channel("<EMBD_BLK>")
error = error_handler.get(logger)

DEFAULT_HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HOME = Path.home()

@module(
    "EEB12558-B4FA-4F34-A9FD-3F5890E9CD3F",
    "EmbeddingModule",
    "0.0.1",
    EmbeddingRetrievalTask,
)
class EmbeddingModule(HFBase, ModuleBase):

    def __init__(self, model_config_path) -> None:
        """Initialize
        This function gets called by `.load` and `.train` function
        which initializes this module.
        """
        super().__init__()
        hf_model, _hf_revision = self.read_config(
            model_config_path, DEFAULT_HF_MODEL, None
        )
        self.model = SentenceTransformer(
            hf_model, cache_folder=f"{HOME}/.cache/huggingface/sentence_transformers"
        )

    @classmethod
    def load(cls, model_path: str, **kwargs):
        """Load a caikit model
        Args:
            model_path: str
                Path to caikit model config directory.
        """
        return cls(model_path)

    def run(
            self, input: List[str], **kwargs
    ) -> EmbeddingResult:  # pylint: disable=arguments-differ
        """Run inference on model.
        Args:
            input: List[str]
                Input text to be processed
        Returns:
            EmbeddingResult: the output
        """

        result = self.model.encode(input)

        vectors: List[Vector1D] = []
        for vector in result:
            vectors.append(Vector1D(vector))

        return EmbeddingResult(vectors)
