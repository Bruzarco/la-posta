from os import path

config = {}

config['project_folder'] = path.dirname(path.realpath(__file__))
config['upload_folder'] = path.join(config['project_folder'], 'py/uploads')