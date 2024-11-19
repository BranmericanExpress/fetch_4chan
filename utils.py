# fetcher/utils.py

import os
import json
import logging
from typing import List, Dict, Any


def create_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Creates and configures a logger.

    Parameters
    ----------
    name : str
        Name of the logger.
    log_file : str
        File to output logs to.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    if log_file:
        fh = logging.FileHandler(log_file, mode='a')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def save_to_json(data: List[Dict[str, Any]], filename: str, append: bool = True, logger: logging.Logger = None):
    """
    Saves data to a JSON file using line-delimited JSON format.

    Parameters
    ----------
    data : list of dict
        Data to save.
    filename : str
        File path to save the data.
    append : bool
        Whether to append to existing file.
    logger : logging.Logger
        Logger for logging messages.
    """
    mode = 'a' if append else 'w'
    if logger:
        logger.info(f"Saving data to {filename}")
    try:
        with open(filename, mode) as file:
            for entry in data:
                json_line = json.dumps(entry)
                file.write(f"{json_line}\n")
    except Exception as e:
        if logger:
            logger.error(f"Error saving data to {filename}: {e}")
        raise


def create_directories(board: str, output_dir: str = '.') -> str:
    """
    Creates directories for saving data.

    Parameters
    ----------
    board : str
        Board name.
    output_dir : str
        Base output directory.

    Returns
    -------
    str
        Path to the base directory for the board.
    """
    base_path = os.path.join(output_dir, board)
    images_path = os.path.join(base_path, 'images')
    os.makedirs(images_path, exist_ok=True)
    return base_path


def validate_board_name(board: str):
    """
    Validates that the board name is valid.

    Parameters
    ----------
    board : str
        The board name to validate.

    Raises
    ------
    ValueError
        If the board name is invalid.
    """
    # This list can be updated to include all valid board names
    valid_boards = [
        'po', 'g', 'b', 'hr', 'biz', 'fit', 'pol', 'sci', 'tech', 'news',
        # Add more valid board names here
    ]
    if board not in valid_boards:
        raise ValueError(f"The board '{board}' is not a valid 4chan board.")
