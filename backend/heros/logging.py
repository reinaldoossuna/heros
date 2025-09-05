from heros.config import settings
import logging
import sys

LOGGER = logging.getLogger(__name__)


def setup_logging():
    """Initialize logging to `log_file` and stdout.

    Parameters
    ----------
    log_file : str
        Name of the file that will be logged to.
    """
    stdout_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=[stdout_handler],
        level=settings.log_level.to_logging(),
        format="%(asctime)s: %(message)s",
    )

    # Make sure we log uncaught exceptions
    def exception_logging(type, value, tb):
        LOGGER.exception("Uncaught exception", exc_info=(type, value, tb))

    sys.excepthook = exception_logging

    LOGGER.info("Logging initialized.")
