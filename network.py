# fetcher/network.py

import os
import time
import json
import requests
from typing import Dict, Any
from requests.exceptions import HTTPError, ConnectionError, Timeout
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .utils import save_to_json, create_directories, validate_board_name


class FourChanFetcher:
    """
    A class to fetch threads and images from a specified 4chan board.
    """

    BASE_URL = 'https://a.4cdn.org'
    IMAGE_URL = 'https://i.4cdn.org'

    def __init__(self, board: str, output_dir: str = '.', session: requests.Session = None, logger=None):
        """
        Initializes the FourChanFetcher instance.

        Parameters
        ----------
        board : str
            The board to fetch from (e.g., 'g', 'po').
        output_dir : str
            The directory to save fetched data.
        session : requests.Session
            A requests session object to reuse connections.
        logger
            Logger instance for logging messages.
        """
        validate_board_name(board)
        self.board = board
        self.output_dir = output_dir
        self.session = session or requests.Session()
        self.logger = logger
        self.base_path = create_directories(board, output_dir)
        self.headers = {'User-Agent': 'fetch_4chan/1.0'}

    def fetch_catalog(self) -> Dict[str, Any]:
        """
        Fetches the catalog for the specified board.

        Returns
        -------
        dict
            The catalog data as a dictionary.

        Raises
        ------
        requests.exceptions.RequestException
            If an error occurs while making the HTTP request.
        json.JSONDecodeError
            If the response cannot be decoded as JSON.
        """
        catalog_url = f"{self.BASE_URL}/{self.board}/catalog.json"
        try:
            response = self.session.get(catalog_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            catalog_data = response.json()
            return catalog_data
        except (HTTPError, ConnectionError, Timeout) as e:
            self.logger.error(f"Error fetching catalog: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding catalog JSON: {e}")
            raise

    def fetch_thread(self, thread_no: int) -> Dict[str, Any]:
        """
        Fetches a specific thread from the board.

        Parameters
        ----------
        thread_no : int
            The thread number to fetch.

        Returns
        -------
        dict
            The thread data as a dictionary.

        Raises
        ------
        requests.exceptions.RequestException
            If an error occurs while making the HTTP request.
        json.JSONDecodeError
            If the response cannot be decoded as JSON.
        """
        thread_url = f"{self.BASE_URL}/{self.board}/thread/{thread_no}.json"
        try:
            response = self.session.get(thread_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            thread_data = response.json()
            return thread_data
        except (HTTPError, ConnectionError, Timeout) as e:
            self.logger.error(f"Error fetching thread {thread_no}: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding thread JSON: {e}")
            raise

    def save_thread_starter(self, thread_data: Dict[str, Any]):
        """
        Saves the thread starter post to a JSON file.

        Parameters
        ----------
        thread_data : dict
            The thread data containing posts.
        """
        thread_starter_posts = [
            post for post in thread_data.get('posts', []) if 'sub' in post
        ]
        thread_starter_data = []
        for post in thread_starter_posts:
            data = {
                'no': post['no'],
                'now': post.get('now', ''),
                'name': post.get('name', ''),
                'sub': post.get('sub', ''),
                'time': post.get('time', 0),
                'semantic_url': post.get('semantic_url', ''),
                'replies': post.get('replies', 0),
                'images': post.get('images', 0)
            }
            thread_starter_data.append(data)
        filename = os.path.join(self.base_path, 'thread_list.json')
        save_to_json(thread_starter_data, filename, append=True, logger=self.logger)

    def save_image_posts(self, thread_data: Dict[str, Any], thread_no: int):
        """
        Saves image posts from a thread to a JSON file.

        Parameters
        ----------
        thread_data : dict
            The thread data containing posts.
        thread_no : int
            The thread number for filename reference.
        """
        images_info = [
            {
                'no': post['no'],
                'now': post.get('now', ''),
                'name': post.get('name', ''),
                'com': post.get('com', ''),
                'filename': post.get('filename', ''),
                'ext': post.get('ext', ''),
                'w': post.get('w', 0),
                'h': post.get('h', 0),
                'time': post.get('time', 0),
                'md5': post.get('md5', ''),
                'fsize': post.get('fsize', 0),
                'resto': post.get('resto', 0),
                'url': f"{self.IMAGE_URL}/{self.board}/{post['tim']}{post['ext']}"
            }
            for post in thread_data.get('posts', [])
            if 'tim' in post and 'ext' in post
        ]
        filename = os.path.join(self.base_path, 'images', f"{self.board}-{thread_no}_ImageURLs.json")
        save_to_json(images_info, filename, append=False, logger=self.logger)

    def fetch_and_save_thread(self, thread_no: int):
        """
        Fetches and saves the thread starter and image posts for a given thread.

        Parameters
        ----------
        thread_no : int
            The thread number to fetch.
        """
        try:
            thread_data = self.fetch_thread(thread_no)
            self.logger.info(f"Fetched thread number {thread_no}")
            self.save_thread_starter(thread_data)
            self.logger.info(f"Saved thread starter for thread {thread_no}")
            self.save_image_posts(thread_data, thread_no)
            self.logger.info(f"Saved image posts for thread {thread_no}")
        except Exception as e:
            self.logger.error(f"Failed to process thread {thread_no}: {e}")

    def fetch_top_threads(self, threads: int = 5, offset: int = 0):
        """
        Fetches and processes the top threads from the board concurrently.

        Parameters
        ----------
        threads : int
            Number of threads to fetch.
        offset : int
            Offset to start fetching threads from.
        """
        try:
            catalog = self.fetch_catalog()
            all_threads = []
            for page in catalog:
                all_threads.extend(page.get('threads', []))
            selected_threads = [
                thread['no'] for thread in all_threads[offset:offset + threads]
            ]
            self.logger.info(f"Selected threads: {selected_threads}")

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(self.fetch_and_save_thread, thread_no): thread_no
                    for thread_no in selected_threads
                }
                for future in tqdm(as_completed(futures), total=len(futures), desc='Fetching threads'):
                    thread_no = futures[future]
                    try:
                        future.result()
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        self.logger.error(f"Thread {thread_no} generated an exception: {e}")

        except Exception as e:
            self.logger.error(f"An error occurred while fetching top threads: {e}")
            raise
