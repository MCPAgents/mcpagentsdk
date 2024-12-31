# mpcagent/logger.py

import logging

# Configure logger for MCPAgent
logger = logging.getLogger("mpcagent")
logger.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
)
ch.setFormatter(formatter)

# Add the handler to the logger if not already added
if not logger.handlers:
    logger.addHandler(ch)
