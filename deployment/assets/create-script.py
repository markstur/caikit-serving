import os
import json

MODELS_LIST = json.loads(os.getenv('MODELS_LIST', ["mini", "slate"]))

with open ('../../load-models-config.sh', 'w') as rsh:
    init_models_command = 'cd demo && '
    for model in MODELS_LIST:
        init_models_command += f"cd models/{model} && cd ../../ && cd models/{model}-rr && cd ../../ && cd models/{model}-ss && cd ../../ &&"
    init_models_command += ' cd server && python start_runtime.py'
    rsh.write(init_models_command)