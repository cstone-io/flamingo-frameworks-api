import signal

from dotenv import load_dotenv, find_dotenv
from loguru import logger
import uvicorn

from .app import app
from .utils.config import Config
from .utils.logging import construct_logger
from .utils.sys import cleanup

load_dotenv(find_dotenv())

if __name__ == "__main__":
    config = Config.get()

    logging_kwargs = config.logging.to_dict()
    construct_logger(**logging_kwargs)

    logger.info("Configuration loaded successfully")
    logger.info("Starting server...")

    # Register signal handlers
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    uvicorn_kwargs = config.uvicorn.to_dict()
    uvicorn.run(app, **uvicorn_kwargs)
