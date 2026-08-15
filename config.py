import tomllib
from typing import Any

def read_config() -> dict[str, Any]:
    """Read and return the configuration from the TOML file."""
    config_file = open('config.toml', 'rb')
    config = tomllib.load(config_file)
    config_file.close()
    return config

def write_config(pairs: dict[str, Any]) -> None:
    """Write a key-value pairs to the TOML configuration file."""
    config_file = open('config.toml', 'w')
    for key, value in pairs.items():
        config_file.write("{} = '{}'\n".format(key, value))
    config_file.close()
    return None
