#!/usr/bin/env python
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
import argparse
from os import path
import sys

# First Party
import alog
import caikit

# Add the runtime/library to the path
# sys.path.append(
    # path.abspath(path.join(path.dirname(__file__), "../../"))
# )
# 
# Load configuration for model(s) serving
# CONFIG_PATH = path.realpath(
    # path.join(path.dirname(__file__), "config.yml")
# )
# caikit.configure(CONFIG_PATH)

alog.configure(default_level="debug")


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Bootstrap and save a model for the TextEmbedding module"
    )
    parser.add_argument(
        "-m", "--model-name-or-path", required=True, help="Source model name or path"
    )
    parser.add_argument(
        "-o", "--output-path", required=True, help="Output model config directory"
    )
    args = parser.parse_args()
    return args.model_name_or_path, args.output_path


def main() -> int:
    model_name_or_path, output_path = _parse_args()
    print("MODEL NAME OR PATH: ", model_name_or_path)
    print("OUTPUT PATH:        ", output_path)

    from caikit_nlp.modules.text_embedding import EmbeddingModule as module
    module.bootstrap(model_name_or_path).save(output_path)


if __name__ == "__main__":
    sys.exit(main())
