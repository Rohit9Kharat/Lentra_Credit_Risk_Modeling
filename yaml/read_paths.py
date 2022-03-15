# read_paths.py file

import yaml

with open(r'paths.yaml') as file:
    documents = yaml.full_load(file)

    print(documents)

