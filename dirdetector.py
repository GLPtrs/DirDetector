#!/usr/bin/env python3

import argparse
import sys
import logging
import queue
import threading
import requests

from colorama import init, Fore, Style

init(autoreset=True)

class DirectoryDetector:
    def __init__(self, base_url, wordlist_path, threads=10,
                 extensions=None, valid_statuses=None, delay=0.0, proxy=None):
        self.base_url = base_url.rstrip('/') + '/'
        self.wordlist_path = wordlist_path
        self.threads = threads
        self.extensions = extensions or ['']
        self.valid_statuses = valid_statuses or [200]
        self.delay = delay
        self.proxy = {'http': proxy, 'https': proxy} if proxy else None
        self.found = []
        self.tasks = queue.Queue()
        self.session = requests.Session()

    def load_words(self):
        try:
            with open(self.wordlist_path, 'r') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        yield word
        except IOError as e:
            logging.error(f"Cannot open wordlist: {e}")
            sys.exit(1)

    def build_targets(self):
        for word in self.load_words():
            for ext in self.extensions:
                target = word + (f".{ext}" if ext else '')
                url = self.base_url + target
                self.tasks.put(url)

    def worker(self):
        while True:
            try:
                url = self.tasks.get(timeout=1)
            except queue.Empty:
                return
            try:
                resp = self.session.get(url, timeout=5,
                                        proxies=self.proxy)
                if resp.status_code in self.valid_statuses:
                    self.print_result(url, resp.status_code)
                    self.found.append((url, resp.status_code))
            except requests.RequestException:
                pass
            finally:
                self.tasks.task_done()

    def print_banner(self):
        print(Fore.CYAN + f"[*] Starting directory scan on {self.base_url}"
              f" with {self.threads} threads, extensions={self.extensions}" + Style.RESET_ALL)

    def print_result(self, url, code):
        color = Fore.GREEN if code < 300 else Fore.YELLOW
        print(f"{color}[+] {url} -> {code}{Style.RESET_ALL}")

    def print_summary(self):
        print(Fore.MAGENTA + f"[*] Scan complete: {len(self.found)} valid paths found." + Style.RESET_ALL)

    def run(self):
        self.build_targets()
        self.print_banner()
        threads = []
        try:
            for _ in range(self.threads):
                t = threading.Thread(target=self.worker, daemon=True)
                t.start()
                threads.append(t)
            self.tasks.join()
        except KeyboardInterrupt:
            logging.info("Scan interrupted by user (Ctrl+C). Exiting...")
        finally:
            self.print_summary()
            self.session.close()


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt="%H:%M:%S")
    parser = argparse.ArgumentParser(description="Python Web Directory Detector")
    parser.add_argument('-u', '--url', required=True,
                        help='Base URL (e.g., http://example.com)')
    parser.add_argument('-w', '--wordlist', required=True,
                        help='Path to wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=10,
                        help='Number of concurrent threads')
    parser.add_argument('-x', '--extensions', nargs='*', default=[''],
                        help='File extensions (e.g., php html txt)')
    parser.add_argument('-s', '--status', nargs='*', type=int,
                        default=[200], help='HTTP status codes to report')
    parser.add_argument('--delay', type=float, default=0.0,
                        help='Delay between requests in seconds')
    parser.add_argument('--proxy', help='Proxy URL (e.g., http://127.0.0.1:8080)')
    args = parser.parse_args()

    detector = DirectoryDetector(
        base_url=args.url,
        wordlist_path=args.wordlist,
        threads=args.threads,
        extensions=args.extensions,
        valid_statuses=args.status,
        delay=args.delay,
        proxy=args.proxy
    )
    detector.run()

if __name__ == '__main__':
    main()