import os
import json

# Variable must contain the path from models dir to where the model's artifacts are located
MODELS_LIST = json.loads(os.getenv('MODELS_LIST', '["sentence-transformers/all-MiniLM-L6-v2/artifacts"]'))

with open ('../../load-models-config.sh', 'w') as rsh:
    init_models_command = 'cd demo && '
    for model in MODELS_LIST:
        init_models_command += f"cd models/{model} && cd ../../../../ &&"
    init_models_command += ' cd server'
    rsh.write(init_models_command)