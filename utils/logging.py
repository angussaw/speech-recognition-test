import logging
import logging.config
import os
from pathlib import Path

import yaml

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = BASE_DIR / "logs"
CONF_DIR = BASE_DIR / "conf"

LOGS_DIR.mkdir(exist_ok=True)


def setup_logging(env: str = "base") -> logging.Logger:
    """
    Set up logging configuration.

    This function loads the logging configuration from a YAML file and sets up
    the logger. If the configuration file is not found, it falls back to basic
    logging configuration.

    Args:
        env (str): The environment to load the configuration for.
                   Defaults to 'base'.

    Returns:
        logging.Logger: Configured logger object.

    Raises:
        FileNotFoundError: If the specified logging configuration file doesn't
                           exist.
        yaml.YAMLError: If there's an error parsing the YAML configuration file.
    """
    config_path = CONF_DIR / env / "logging.yaml"

    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)

            # Replace ${LOGS_DIR} with the actual path
            config = _update_config_paths(config, str(LOGS_DIR))

            logging.config.dictConfig(dict(config))
        except yaml.YAMLError as e:
            logging.basicConfig(level=logging.INFO)
            logging.error(f"Error parsing YAML configuration: {e}")
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging configuration file not found: {config_path}")

    return logging.getLogger("root")


def _update_config_paths(config: dict | list, logs_dir: str) -> dict | list:
    """
    Recursively update paths in the logging configuration.

    This function replaces ${LOGS_DIR} placeholders with the actual logs
    directory path.

    Args:
        config (Union[Dict, List]): The configuration dictionary or list to
                                    update.
        logs_dir (str): The actual path to the logs directory.

    Returns:
        Union[Dict, List]: The updated configuration with replaced paths.
    """
    if isinstance(config, dict):
        for k, v in config.items():
            if isinstance(v, str) and "${LOGS_DIR}" in v:
                config[k] = v.replace("${LOGS_DIR}", logs_dir)
            elif isinstance(v, dict | list):
                _update_config_paths(v, logs_dir)
    elif isinstance(config, list):
        for i, v in enumerate(config):
            if isinstance(v, str) and "${LOGS_DIR}" in v:
                config[i] = v.replace("${LOGS_DIR}", logs_dir)
            elif isinstance(v, dict | list):
                _update_config_paths(v, logs_dir)
    return config


# Create the logger
logger = setup_logging()
