# Fetch 4chan

## Overview

Fetch 4chan is a Python-based tool designed to fetch threads and images from specified boards on 4chan. The script retrieves the top threads and associated images based on user-defined parameters and stores them in organized JSON files for easy access and analysis. The tool is built with error handling, efficient networking, and logging to ensure robust and reliable data fetching.

## Features

- Fetch and save top threads and associated images from a specified 4chan board.
- Flexible command-line interface to specify boards, number of threads, and output directories.
- Concurrent fetching of threads for improved performance.
- Detailed logging of actions and errors to both console and log files.
- Rate limiting to avoid overwhelming 4chan's servers.
- Customizable output directory for organized data storage.
- Extensible and modular code structure for easy maintenance and future improvements.

## Project Structure

```plaintext
fetch_4chan/
├── fetcher/
│   ├── __init__.py
│   ├── network.py
│   ├── utils.py
├── scripts/
│   └── fetch_threads.py
└── setup.py
```

- `fetcher/`: Contains the main fetching logic and utility functions.
  - `__init__.py`: Initializes the `fetcher` package and imports key classes and functions.
  - `network.py`: Contains the `FourChanFetcher` class for network operations.
  - `utils.py`: Contains utility functions for logging, saving data, directory creation, and board validation.
- `scripts/`: Contains the entry point for executing the fetching process.
  - `fetch_threads.py`: Main script to fetch threads and images from 4chan.
- `setup.py`: Setup file for packaging and installing the module.

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Install Dependencies

First, clone the repository to your local machine:

```sh
git clone https://github.com/BranmericanExpress/fetch_4chan.git
cd fetch_4chan
```

Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Install the Package

You can install the package locally in editable mode:

```sh
pip install -e .
```

## Usage

To use the script, navigate to the `fetch_4chan` directory and run the `fetch_threads.py` script with the desired options:

```sh
python scripts/fetch_threads.py -b g -t 5 -o 0 -d data
```

### Command-Line Arguments

- `-b, --board`: The board to fetch from (e.g., `po`, `g`, etc.). **Required.**
- `-t, --threads`: Number of threads to fetch. **Default is 5.**
- `-o, --offset`: Offset to start fetching threads from. **Default is 0.**
- `-d, --directory`: Output directory for saving data. **Default is the current directory (`.`).**

### Example

To fetch the top 5 threads starting from the 6th thread and save the images from the 'g' board into the `data` directory:

```sh
python scripts/fetch_threads.py -b g -t 5 -o 5 -d data
```

## Logging

The script logs messages to both the console and a log file named `fetch_4chan.log` located in the current directory. The log messages include timestamps, log levels, and detailed messages about the script's actions and any errors encountered.

## Error Handling

The script includes comprehensive error handling to manage HTTP errors, connection issues, and JSON decoding errors. All errors are logged with detailed messages to help with troubleshooting.

## Customization

The code is modular and can be easily extended or customized. Here are some potential customization points:

- **Adding new boards**: Update the `valid_boards` list in the `validate_board_name` function in `utils.py`.
- **Modifying logging configuration**: Adjust the `create_logger` function in `utils.py` to change logging settings.
- **Rate limiting**: Modify the `time.sleep(1)` call in the `fetch_and_save_thread` method in `network.py` to change the delay between requests.