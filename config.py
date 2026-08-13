import tomllib

def read_config():
    config_file = open('config.toml', 'rb')
    config = tomllib.load(config_file)
    config_file.close()
    return config

def write_config(key, value):
    config_file = open('config.toml', 'w')
    config_file.write("{} = '{}'\n".format(key, value))
    config_file.close()
    return None
