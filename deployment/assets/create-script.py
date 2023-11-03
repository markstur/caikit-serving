import os
import json

MODELS_LIST_VAR = json.dumps(os.getenv('MODELS_LIST')) if os.getenv('MODELS_LIST') else  '["mini/artifacts"]'
MODELS_LIST = json.loads(MODELS_LIST_VAR)

with open ('../../load-models-config.sh', 'w') as rsh:
    init_models_command = 'cd demo && '
    for model in MODELS_LIST:
        init_models_command += f"cd models/{model} && cd ../../../ &&"
    init_models_command += ' cd server'
    rsh.write(init_models_command)