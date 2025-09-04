import yaml
from utils import MONGO,JINJA_FILES_STRACTIRE,TAXES,RATES


def yaml_loader(file_name):
    with open(file_name, 'r') as file:
            config = yaml.safe_load(file)
            return config
    

general_conf = yaml_loader("conf.yaml")
mongo_conf = general_conf[MONGO]
jinja_stractures_conf= general_conf[JINJA_FILES_STRACTIRE]
taxes_conf = general_conf[TAXES]
rates_conf = general_conf[RATES]