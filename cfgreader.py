import yaml
config = lambda: None

with open(r'/workspace/config.yaml') as file:
    documents = yaml.full_load(file)
    for item, doc in documents.items():
        setattr(config, item, doc)
