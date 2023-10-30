# Caikit Text Embedding

Caikit service for embeddings.

| Task                    | Module(s)                                      | Salient Feature(s)                                                                                                                                                         |
|-------------------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EmbeddingTask           | `TextEmbedding`                             | text/embedding from a local sentence-transformers model                                                                                                                 
| EmbeddingTasks          | `TextEmbedding`                             | Same as EmbeddingTask but multiple sentences (texts) as input and corresponding list of outputs.                                                                        
| SentenceSimilarityTask  | `TextEmbedding`                             | text/sentence-similarity from a local sentence-transformers model (Hugging Face style API returns scores only in order of input sentences)                              |
| SentenceSimilarityTasks | `TextEmbedding`                             | Same as SentenceSimilarityTask but multiple source_sentences (each to be compared to same list of sentences) as input and corresponding lists of outputs.               |
| RerankTask              | `TextEmbedding`                             | text/rerank from a local sentence-transformers model (Cohere style API returns top_n scores in order of relevance with index to source and optionally returning inputs) |
| RerankTasks             | `TextEmbedding`                             | Same as RerankTask but multiple queries as input and corresponding lists of outputs. Same list of documents for all queries.                                            |


### Before Starting

The following tools are required:

- [python](https://www.python.org) (v3.8+)
- [pip](https://pypi.org/project/pip/) (v23.0+)

**Note:** Before installing dependencies and to avoid conflicts in your environment, it is advisable to use a virtual environment. The subsection which follows provides an example of a virtual environment, Python venv.

#### Setting Up Virtual Environment using Python venv

For [(venv)](https://docs.python.org/3/library/venv.html), make sure you are in an activated `venv` when running `python` in the example commands that follow. Use `deactivate` if you want to exit the `venv`.

Install the dependencies: `pip install -r requirements.txt`

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Models

To create a model configuration and artifacts, the best practice is to run the module's bootstrap() and save() methods.  This will:

* Load the model by name (from Hugging Face hub or repository) or from a local directory. The model is loaded using the sentence-transformers library.
* Save a config.yml which:
  * Ties the model to the module (with a module_id GUID)
  * Sets the artifacts_path to the default "artifacts" subdirectory
  * Saves the model in the artifacts subdirectory

This can be done by running the `boostrap_model.py` script in your virtual environment.

```shell
source venv/bin/activate
cd demo/server
./bootstrap_model.py -m <MODEL_NAME_OR_PATH> -o <OUTPUT_DIR>
```

To avoid overwriting your files, the save() will return an error if the output directory already exists. You may want to use a temporary name. After success, move the output directory to a `<model-id>` directory under your local models dir.

> You can use the same process for cluster deployment, by copying the output directory to your cluster storage.
> Check [Onboarding Models Documentation](./deployment/README.md#onboarding-models) in the deployment instructions to read more about how the models are loaded at deploy time.

### Starting the Caikit Runtime

In one terminal, start the runtime server:

```shell
source venv/bin/activate
cd demo/server
python start_runtime.py
```

### Embedding retrieval example Python client

In another terminal, run the example client code to retrieve embeddings.

```shell
source venv/bin/activate
cd demo/client
MODEL=<model-id> python embeddings.py
```

The client code calls the model and queries for embeddings using 2 example sentences.

You should see output similar to the following:

```ShellSession
$ python embeddings.py
INPUT TEXTS:  ['test first sentence', 'another test sentence']
RESULTS: [
   [0.02021969109773636, 0.07058270275592804, 0.008317082189023495, ...]
   [0.04209445044398308, 0.07522737234830856, 0.018512120470404625, ...]
]
LENGTH:  2  x  384
```

### Sentence similarity example Python client

In another terminal, run the client code to infer sentence similarity.

```shell
source venv/bin/activate
cd demo/client
MODEL=<model-id> python sentence_similarity.py
```

The client code calls the model and queries sentence similarity using 1 source sentence and 2 other sentences (hardcoded in sentence_similarity.py). The result produces the cosine similarity score by comparing the source sentence with each of the other sentences.

You should see output similar to the following:

```ShellSession
$ python sentence_similarity.py   
SOURCE SENTENCE:  first sentence
SENTENCES:  ['test first sentence', 'another test sentence']
RESULTS:  [0.6898421049118042, 0.5583217144012451]
```

### Reranker example Python client

In another terminal, run the client code to execute the reranker task using both gRPC and REST.

```shell
source venv/bin/activate
cd demo/client
MODEL=<model-id> python reranker.py
```

You should see output similar to the following:

```ShellSession
$ python reranker.py
======================
TOP N:  3
QUERIES:  ['first sentence', 'any sentence']
DOCUMENTS:  [{'text': 'first sentence', 'title': 'first title'}, {'_text': 'another sentence', 'more': 'more attributes here'}, {'text': 'a doc with a nested metadata', 'meta': {'foo': 'bar', 'i': 999, 'f': 12.34}}]
======================
RESPONSE from gRPC:
===
QUERY:  first sentence
  score: 1.0000001192092896  index: 0  text: first sentence
  score: 0.6204259991645813  index: 1  text: another sentence
  score: 0.11101679503917694  index: 2  text: a doc with a nested metadata
===
QUERY:  any sentence
  score: 0.5091423988342285  index: 1  text: another sentence
  score: 0.42496341466903687  index: 0  text: first sentence
  score: 0.0962495356798172  index: 2  text: a doc with a nested metadata
===================
RESPONSE from HTTP:
{
    "results": [
        {
            "query": "first sentence",
            "scores": [
                {
                    "document": {
                        "text": "first sentence",
                        "title": "first title"
                    },
                    "index": 0,
                    "score": 1.0000001192092896,
                    "text": "first sentence"
                },
                {
                    "document": {
                        "_text": "another sentence",
                        "more": "more attributes here"
                    },
                    "index": 1,
                    "score": 0.6204259991645813,
                    "text": "another sentence"
                },
                {
                    "document": {
                        "text": "a doc with a nested metadata",
                        "meta": {
                            "foo": "bar",
                            "i": 999,
                            "f": 12.34
                        }
                    },
                    "index": 2,
                    "score": 0.11101679503917694,
                    "text": "a doc with a nested metadata"
                }
            ]
        },
        {
            "query": "any sentence",
            "scores": [
                {
                    "document": {
                        "_text": "another sentence",
                        "more": "more attributes here"
                    },
                    "index": 1,
                    "score": 0.5091423988342285,
                    "text": "another sentence"
                },
                {
                    "document": {
                        "text": "first sentence",
                        "title": "first title"
                    },
                    "index": 0,
                    "score": 0.42496341466903687,
                    "text": "first sentence"
                },
                {
                    "document": {
                        "text": "a doc with a nested metadata",
                        "meta": {
                            "foo": "bar",
                            "i": 999,
                            "f": 12.34
                        }
                    },
                    "index": 2,
                    "score": 0.0962495356798172,
                    "text": "a doc with a nested metadata"
                }
            ]
        }
    ]
}
```

### Try the REST API using the FastAPI GUI

The server is configured to serve a REST API UI with a FastAPI UI at: http://0.0.0.0:8080/docs (running locally).

* Follow the link: http://0.0.0.0:8080/docs
* Click on the `POST` to expand it
* Click on the `Try it out` button to test it
* Enter `mini` as the **model_id**
* Click the `Execute` button

You can edit the **Request body** as shown below to test with multiple input sentences.

![fastapi](doc/images/fastapi.png)

Scroll down to see:

* the resulting **Response body**
* how to run the request with curl
* additional API documentation

### Try grpcui

The server is configured to support gRPC with reflection. This is used by the infer_model.py client above. If you'd like to explore with the `grpcui` client, follow these steps:

1. Install grpcui
2. Run `grpcui -plaintext 0.0.0.0:8085`
3. Select the **Service name** and **Method name** as shown below
4. Under **Request Metadata** set **Name** to `mm-model-id` and **Value** to `mini`
5. Under **Request Data** click on `Add item` one or more times to add input sentences
6. Click the `Invoke` button

The request form will look like this:

![grpc_request_form](doc/images/grpc_request_form.png)

After you hit `Invoke`, it will show the response like this:

![grpc_response](doc/images/grpc_response.png)

Use the **Request Form** or **History** tab to try another request or retry a recent one.

### Using Caikit to dump interfaces

If you need proto files, you can ask a properly configured caikit runtime to dump them to a directory.  This will also save the openapi.json for HTTP/REST.

In a terminal, use your virtual environment and run `dump_apis.sh`:

> Note: This will start and stop the server, so make sure you don't have one already running.

```shell
source venv/bin/activate
cd demo/client
./dump_apis.sh
```

This will create a directory named `generated_interfaces` under `demo/client` containing all the proto files (and the openapi.json file).
