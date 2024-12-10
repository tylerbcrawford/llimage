"""
LLiMage - Advanced PDF Image and Chart Analysis Library
"""

import json
import logging.config
import os
from pathlib import Path

__version__ = "0.2.0"

# Setup paths
ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = ROOT_DIR / "config"
LOGS_DIR = ROOT_DIR / "logs"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# Load logging configuration
def setup_logging():
    """Configure logging using the logging.json configuration file."""
    logging_config_path = CONFIG_DIR / "logging.json"
    if logging_config_path.exists():
        with open(logging_config_path) as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging configuration not found at {logging_config_path}")

# Load default configuration
def load_config():
    """Load the default configuration from default.json."""
    config_path = CONFIG_DIR / "default.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    else:
        logging.warning(f"Default configuration not found at {config_path}")
        return {}

# Initialize logging
setup_logging()

# Initialize configuration
config = load_config()

# Create logger for this module
logger = logging.getLogger(__name__)
logger.info(f"Initializing LLiMage v{__version__}")

# Import submodules
from . import chart
from . import image
from . import output

__all__ = ["chart", "image", "output", "config", "logger"]
