from contextlib import contextmanager
import inspect
import logging
import sys
from typing import Generator, Optional

from loguru import logger


class LoggerStream:
    """
    A custom stream (file-like object) to intercept writes (like print statements)
    and redirect them to the loguru logger.

    Typical usage involves replacing sys.stdout with an instance of this class to
    capture `print` statements and forward them to loguru.

    NOTE: The module and line number of the caller will be captured and included in
    the log message!

    Attributes:
        level (str): The log level at which messages will be logged.
                     It must be one of loguru's valid levels (e.g., "INFO", "DEBUG").

    Example:
        sys.stdout = LoggerStream(level="INFO")
        print("This message will be logged instead of printed.")
    """

    def __init__(self, level: str) -> None:
        self.level = level

    def write(self, message: str) -> None:
        if message := message.rstrip():
            # Get the frame that called print()
            frame = inspect.currentframe()
            while frame:
                frame = frame.f_back
                if frame.f_globals["__name__"] != __name__:
                    break

            # Extract necessary information from the frame
            # This fixes bug when using this class with enqueued log messages
            frame_info = {
                "filename": frame.f_code.co_filename,
                "line_no": frame.f_lineno,
                "function": frame.f_code.co_name,
            }

            # Use the captured frame info for logging context
            logger.bind(captured_frame_info=frame_info).opt(depth=1).log(
                self.level, message
            )

    def flush(self) -> None:
        pass


@contextmanager
def capture_prints(level: str = "PRINT") -> Generator:
    """
    A context manager to temporarily capture print statements and log them using loguru.

    NOTE: The module and line number of the caller will be captured and included in
    the log message just like calling the logger directly!

    :param level: Log level to use. See Loguru documentation for more details.
    """
    # Check if the desired log level exists
    try:
        logger.level(level)
    except ValueError:
        logger.warning(f"Log level '{level}' not found. Defaulting to 'INFO'.")
        level = "INFO"

    original_stdout = sys.stdout
    sys.stdout = LoggerStream(level=level)
    try:
        yield
    finally:
        sys.stdout = original_stdout


def custom_format(record) -> str:
    """
    Custom log formatter function. Maintains the default loguru format but splits
    multi-line messages to start on a new line. This keeps things like tables formatted
    correctly.

    Example:
        2023-08-10 15:00:00 | INFO     | __main__:<module>:1 - Single line message!
        2023-08-10 15:00:00 | INFO     | __main__:<module>:1 - \n
        This is a multi-line message! Notice we start on a new line. \n
        Here is the second line.

    :param record: Dictionary containing log details.
    :return: Formatted log string.
    """
    # Check if the message contains line breaks
    if "\n" in record["message"]:
        # Modify the format to start the message on a new line
        format_string = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>\n{message}</level>\n"
    else:
        format_string = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"

    return format_string

class InterceptHandler(logging.Handler):
    """
    Custom logging handler to propagate logs from the standard library to loguru.
    """

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = logging.currentframe()
        depth = 0
        while frame:
            if (
                frame.f_code.co_filename == logging.__file__
                or frame.f_code.co_filename == __file__
            ):
                frame = frame.f_back
                depth += 1
                continue
            break

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def construct_logger(
    level: str = "INFO",
    path: Optional[str] = None,
    enqueue: bool = False,
    backtrace: bool = False,
    diagnose: bool = False,
) -> None:
    """
    Function to set up the Loguru logger.

    NOTE: If `buffer` is set to True make sure a file sink is added later on and
        the buffer is cleared. Otherwise, a memory leak will occur.

    :param level: Log level to use. See Loguru documentation for more details.
    :param path: Path to the log file. If None, logs will be printed to stderr.
    :param buffer: Bool flag for using a buffer sink. If True, you can delay the
        log file creation until some later time. This is useful if you want to
        log to a file but don't know the path yet.
    :param enqueue: Bool flag for enqueuing messages. Allows logging with
        multiple processes.
    :param backtrace: Bool flag for including backtrace in log messages. High
        performance impact, use with caution.
    :param diagnose: Bool flag for including diagnostic information in log
        messages. High performance impact, use with caution.
    """
    # Remove all default sinks
    logger.remove()

    # add custom log level for captured print statements (if it doesn't already exist)
    try:
        logger.level("PRINT")
    except ValueError:
        logger.level("PRINT", no=25, color="<white>", icon="󰐪")

    # forward logs from the standard library to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=level)

    # recreate the stderr handler with the desired log level and enqueue
    if path is not None:
        logger.add(
            sink=path,
            level=level,
            enqueue=enqueue,
            backtrace=backtrace,
            diagnose=diagnose,
            format=custom_format,
        )

    logger.add(
        sink=sys.stderr,
        level=level,
        enqueue=enqueue,
        backtrace=backtrace,
        diagnose=diagnose,
        format=custom_format,
    )


@contextmanager
def suppress_logs():
    """
    Context manager to temporarily suppress all logging.
    """
    logger.disable(None)

    try:
        yield
    finally:
        logger.enable(None)
