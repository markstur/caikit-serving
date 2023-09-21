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
from caikit_embeddings.modules.sentence_similarity import SentenceSimilarityTask
from caikit.interfaces.common.data_model.primitive_sequences import FloatSequence

from sentence_transformers import SentenceTransformer, util

from ..hf_base import HFBase

from pathlib import Path
from typing import List

logger = alog.use_channel("<EMBD_BLK>")
error = error_handler.get(logger)

DEFAULT_HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HOME = Path.home()

@module(
    "B7F50AAB-80CE-4D33-BA95-E9E29C4E12E3",
    "SentenceSimilarity",
    "0.0.1",
    SentenceSimilarityTask,
)
class SentenceSimilarity(HFBase, ModuleBase):

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
            self, source_sentence: str, sentences: List[str], **kwargs
    ) -> FloatSequence:  # pylint: disable=arguments-differ
        """Run inference on model.
        Args:
            source_sentence: str
            sentences: List[str]
                Sentences to compare to source_sentence
        Returns:
            FloatSequence
        """

        source_embedding = self.model.encode(source_sentence)
        embeddings = self.model.encode(sentences)

        res = util.cos_sim(source_embedding, embeddings)
        return FloatSequence(res.tolist()[0])
