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

import os
import alog
from caikit.core import module, ModuleBase
from caikit.core.exceptions import error_handler
from caikit_embeddings.data_model.reranker import RerankPrediction, RerankQueryResult, RerankScore, RerankDocuments
from caikit_embeddings.modules.reranker import RerankTask

from sentence_transformers.util import semantic_search, normalize_embeddings, dot_score

from ..hf_base import HFBase

from typing import List

logger = alog.use_channel("<EMBD_BLK>")
error = error_handler.get(logger)


@module(
    "00110203-0405-0607-0809-0a0b02dd0e0f",
    "RerankerModule",
    "0.0.1",
    RerankTask,
)
class Rerank(HFBase, ModuleBase):

    def __init__(self, model_config_path) -> None:
        """Initialize
        This function gets called by `.load` and `.train` function
        which initializes this module.
        """
        super().__init__(model_config_path)

    @classmethod
    def load(cls, model_path: str, **kwargs):
        """Load a caikit model
        Args:
            model_path: str
                Path to caikit model config directory.
        """
        return cls(model_path)

    def run(self, queries: List[str], documents: RerankDocuments, top_n: int = 10) -> RerankPrediction:
        """Run inference on model.
        Args:
            queries: List[str]
            documents:  RerankDocuments
            top_n:  int
        Returns:
            RerankPrediction
        """

        if len(queries) < 1:
            return RerankPrediction()

        if len(documents.documents) < 1:
            return RerankPrediction()

        if top_n < 1:
            top_n = 10  # Default to 10 (to avoid JSON default 0)

        # Using input document dicts so get "text" else "_text" else default to ""
        doc_texts = [srd.document.get("text") or srd.document.get("_text", "") for srd in documents.documents]

        doc_embeddings = self.model.encode(doc_texts, convert_to_tensor=True)
        doc_embeddings = doc_embeddings.to(self.model.device)
        doc_embeddings = normalize_embeddings(doc_embeddings)

        query_embeddings = self.model.encode(queries, convert_to_tensor=True)
        query_embeddings = query_embeddings.to(self.model.device)
        query_embeddings = normalize_embeddings(query_embeddings)

        res = semantic_search(query_embeddings, doc_embeddings, top_k=top_n, score_function=dot_score)

        for r in res:
            for x in r:
                x['document'] = documents.documents[x['corpus_id']].document

        results = [RerankQueryResult([RerankScore(**x) for x in r]) for r in res]

        return RerankPrediction(results=results)
