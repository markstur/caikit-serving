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

# First Party
from caikit.core import TaskBase, task
from caikit.interfaces.common.data_model.primitive_sequences import FloatSequence

from typing import List


@task(
    required_parameters={"source_sentence": str, "sentences": List[str]},
    output_type=FloatSequence
)
class SentenceSimilarityTask(TaskBase):
    pass
