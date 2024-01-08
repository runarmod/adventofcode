"""
A simple script to download all inputs for all saved days and years.
The script assumes that the folder-structure is as follows:

├── 2015
│   ├── 01
│   │   └── <2015 day 1 files>
│   ├── 02
│   │   └── <2015 day 2 files>
│   └── ...
├── 2016
│   ├── 01
│   │   └── <2016 day 1 files>
│   └── ...
└── ...

It will only download inputs for days that are not already downloaded and
which have a folder ready.
"""

import datetime
import os
import sys
import time
from typing import Generator

import requests
from colorama import Fore
from colorama import init as colorama_init
from dotenv import load_dotenv
from tqdm import trange

colorama_init(autoreset=True)
load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit(f"{Fore.YELLOW}COOKIE not found in .env")

ROOT_PATH = os.path.join(os.path.dirname(__file__), "..")


class Logging:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        self.day = 0
        self.year = 1970

        self.years_not_found = 0
        self.days_not_found = 0
        self.inputs_already_exists = 0
        self.inputs_downloaded = 0

    def set_day(self, day: int):
        self.day = day

    def set_year(self, year: int):
        self.year = year

    def start_download(self, year: int, day: int):
        self.set_year(year)
        self.set_day(day)
        if self.verbose:
            print(
                f"{Fore.CYAN}Downloading input for {self.year} day {self.day}...",
                end="\r",
            )

    def year_not_found(self):
        self.years_not_found += 1
        if self.verbose:
            print(f"{Fore.YELLOW}Year {self.year} not found.")

    def day_not_found(self):
        self.days_not_found += 1
        if self.verbose:
            print(f"{Fore.YELLOW}Day {self.day} not found for year {self.year}.")

    def input_already_exists(self):
        self.inputs_already_exists += 1
        if self.verbose:
            print(
                f"{Fore.YELLOW}Input file already exists for day {self.day} for year {self.year}."
            )

    def downloaded(self):
        self.inputs_downloaded += 1
        if self.verbose:
            print(f"{Fore.GREEN}Input day {self.day} for year {self.year} downloaded.")

    def summarize(self):
        print(self)

    def __str__(self):
        return (
            f"Years not found in repo: {Fore.YELLOW}{self.years_not_found}{Fore.RESET}\n"
            f"Days not found in repo: {Fore.YELLOW}{self.days_not_found}{Fore.RESET}\n"
            f"Inputs already exists: {Fore.CYAN}{self.inputs_already_exists}{Fore.RESET}\n"
            f"Inputs downloaded: {Fore.GREEN}{self.inputs_downloaded}{Fore.RESET}"
        )


def get_years_and_days_to_download(
    logger: "Logging",
) -> Generator[tuple[int, int], None, None]:
    """Yields all years and days that should be downloaded."""
    years = trange(2015, datetime.datetime.now().year + 1)
    days = trange(1, 26, leave=False)

    if logger.verbose:
        years = range(2015, datetime.datetime.now().year + 1)
        days = range(1, 26)

    for year in years:
        logger.set_year(year)
        year_path = os.path.join(ROOT_PATH, str(year))

        if not os.path.isdir(year_path):
            logger.year_not_found()
            continue

        for day in days:
            logger.set_day(day)
            day_path = os.path.join(year_path, str(day).zfill(2))

            if not os.path.isdir(day_path):
                logger.day_not_found()
                continue

            input_file_path = os.path.join(day_path, "input.txt")
            if os.path.isfile(input_file_path):
                logger.input_already_exists()
                continue

            yield year, day


def download_input(year: int, day: int, logger: "Logging") -> None:
    """Downloads the input for the given year and day."""
    URL = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": COOKIE}
    USER_AGENT = (
        "ONE-TIME USAGE TO GET ALL INPUTS ON 2nd PC SINCE NO INPUTS ARE SAVED ON MY GITHUB: "
        + "github.com/runarmod/adventofcode/blob/main/utils/inputDownloader.py by runarmod@gmail.com"
    )
    headers = {"User-Agent": USER_AGENT}

    page = requests.get(URL, cookies=cookies, headers=headers)
    if page.status_code != 200:
        sys.exit(
            f"{Fore.RED}Input download failed\nError: {page.status_code}\n{page.content}"
        )

    input_path = os.path.join(ROOT_PATH, str(year), str(day).zfill(2), "input.txt")

    with open(input_path, "w") as f:
        f.write(page.text)

    logger.downloaded()
    time.sleep(1)


def download_inputs(logger: "Logging") -> None:
    for year, day in get_years_and_days_to_download(logger):
        logger.start_download(year, day)
        download_input(year, day, logger)
    logger.summarize()


def main() -> None:
    if "--verbose" in sys.argv:
        logger = Logging(True)
    else:
        print(
            f"{Fore.CYAN}To see more verbose output, run the script with the --verbose flag."
        )
        logger = Logging(False)

    download_inputs(logger)


if __name__ == "__main__":
    main()
