import logging
import sys
from types import FrameType
from typing import Optional


def cleanup(signum: int, frame: Optional[FrameType]) -> None:
    """
    Helper function to handle signals and exit gracefully.

    :param signum: The signal number
    :param frame: The interrupted stack frame
    """
    logging.info("Received signal:", signum, ". Cleaning up...")
    sys.exit(0)
