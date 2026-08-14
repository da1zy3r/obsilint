import tomllib
from typing import Any

def read_config() -> dict[str, Any]:
    """Read and return the configuration from the TOML file."""
    config_file = open('config.toml', 'rb')
    config = tomllib.load(config_file)
    config_file.close()
    return config

def write_config(key: str, value: str) -> None:
    """Write a key-value pair to the TOML configuration file."""
    config_file = open('config.toml', 'w')
    config_file.write("{} = '{}'\n".format(key, value))
    config_file.close()
    return None
