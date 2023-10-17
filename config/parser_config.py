from configparser import ConfigParser
import os
# нужно будет указать путь к файлу а то он не читается через эту хуйню

def read_config(name_file, name_key, name_value):
    config = ConfigParser()
    config.read(os.path.abspath(__file__).replace(os.path.basename(__file__), '') + name_file, encoding="utf-8")
    return config[name_key][name_value]

def write_config(name, surname, id):
    pass

