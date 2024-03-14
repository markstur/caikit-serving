FROM registry.access.redhat.com/ubi9/python-39

RUN pip install -U pip setuptools wheel

COPY remote_models_config.yaml /app/remote_models_config.yaml
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV RUNTIME_LIBRARY='caikit_nlp'

CMD [ "python3", "-m", "caikit.runtime" ]