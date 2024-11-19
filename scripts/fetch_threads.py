# scripts/fetch_threads.py
import sys
import os
import argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fetcher.network import FourChanFetcher
from fetcher.utils import create_logger

def main():
    parser = argparse.ArgumentParser(description="Fetch threads and images from 4chan")
    parser.add_argument(
        '-b', '--board', type=str, required=True,
        help="The board to fetch from (e.g., po, g, etc.)"
    )
    parser.add_argument(
        '-t', '--threads', type=int, default=5,
        help="Number of threads to fetch"
    )
    parser.add_argument(
        '-o', '--offset', type=int, default=0,
        help="Offset to start fetching threads from"
    )
    parser.add_argument(
        '-d', '--directory', type=str, default='.',
        help="Output directory for saving data"
    )
    args = parser.parse_args()

    logger = create_logger('fetch_4chan', log_file='fetch_4chan.log')
    logger.info(f"Starting fetching process for board: {args.board}")

    try:
        fetcher = FourChanFetcher(
            board=args.board,
            output_dir=args.directory,
            logger=logger
        )
        fetcher.fetch_top_threads(threads=args.threads, offset=args.offset)
        logger.info("Fetching process completed successfully.")
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        print(f"Error: {ve}. Please check the board name and try again.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An unexpected error occurred: {e}. Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
