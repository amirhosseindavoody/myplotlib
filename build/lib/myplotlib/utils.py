import random
import string
import sys
import os

from loguru import logger


def random_id(n=6):
    """Get a random id of a given length from alphabetical values."""
    alphabet = string.ascii_lowercase

    return "".join(random.choices(alphabet, k=n))


def count_subfolders(directory_path):
    # Get the list of items in the directory
    items = os.listdir(directory_path)

    # Filter out only the directories
    subfolders = [
        item for item in items if os.path.isdir(os.path.join(directory_path, item))
    ]

    # Count the number of subfolders
    subfolder_count = len(subfolders)

    return subfolder_count


def setup_logger(filename):
    format = "{time:YYYY-MM-DD - HH:mm:ss} - {file}:{line} - {level} - {message}"
    logger.remove()
    handler_id = logger.add(
        sys.stdout,
        colorize=False,
        format=format,
    )
    if filename:
        logger.add(filename, format=format, mode="w")
        logger.info("Log file: {}", filename)
        logger.remove(handler_id)
