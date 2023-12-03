import logging
import os
import signal

import openai
import uvicorn

from .app import app
from .utils.exit import cleanup


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ["LOGGING_LEVEL"],
        format=os.environ["LOGGING_FORMAT"],
    )
    logging.info("Running app startup...")

    # Register signal handlers
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    openai.api_key = os.environ["OPENAI_API_KEY"]

    uvicorn.run(
        app,
        host=os.environ["UVICORN_HOST"],
        port=int(os.environ["UVICORN_PORT"]),
    )
