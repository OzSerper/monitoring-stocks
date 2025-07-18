from jinja2 import Template
import json
from jinja2 import Environment, FileSystemLoader
import hashlib

env = Environment(loader=FileSystemLoader("jinjas_template"))

def stock_add_load_jinja(jinja_file,**data):
    template = env.get_template(jinja_file)
    rendered = template.render(**data)
    json_compitable = json.loads(rendered)
    return json_compitable


def hash_creator(text):
    text_bytes = text.encode('utf-8')
    hash_object = hashlib.sha256(text_bytes)
    return hash_object.hexdigest()