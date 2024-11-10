"""
This script is used to update the stats in the README file.
It downloads the stats from the website and updates the
README file accordingly.
"""

import argparse
import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init

from .config import get_cookie, get_repo_path

colorama_init(autoreset=True)


def update_README(stats: str) -> bool:
    """
    Update the stats in the README file. Returns True
    if the stats were updated. False otherwise.
    """
    REPO_PATH = get_repo_path()
    README_PATH = os.path.join(REPO_PATH, "README.md")

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    replacer = r"<!-- START STATS -->(.|\n)*<!-- END STATS -->"
    replacement = f"<!-- START STATS -->\n```py\n{stats}\n```\n<!-- END STATS -->"

    newContent = re.sub(replacer, replacement, readme_content)

    if newContent == readme_content:
        return False

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(newContent)

    return True


def get_stats_from_HTML(page: requests.Response) -> str:
    """
    Get the stats from the HTML page.
    Returns the stats as a string in the format:
    ```
        [2022] 13*
        [2021] 48*
        ...
        [2015] 50*
    ```
    """
    soup = BeautifulSoup(page.content, "html.parser")
    childsoup = soup.find_all("div", {"class": "eventlist-event"})

    stats = ""
    for element in childsoup:
        year = element.find("a").text
        stars = " 0*"
        span = element.find("span")
        if span is not None:
            stars = span.text
        stats += f"{year} {stars}\n"
    stats = stats.strip()

    total_star_count = soup.find_all("span", {"class": "star-count"})[-1]
    total_star_text = f"\n\nTotal stars: {total_star_count.text}"
    return stats + total_star_text


def update_stats() -> None:
    """
    Update the stats in the README file based on the stats on the website.
    """
    COOKIE = get_cookie()

    URL = "https://adventofcode.com/events"
    cookies = {"session": COOKIE}
    USER_AGENT = "github.com/runarmod/adventofcode by runarmod@gmail.com"
    headers = {"User-Agent": USER_AGENT}
    page = requests.get(URL, cookies=cookies, headers=headers)
    if page.status_code != 200:
        sys.exit(
            f"{Fore.RED}Could not retrieve stats.\nError: {page.status_code}\n{page.content}"
        )

    stats = get_stats_from_HTML(page)
    if update_README(stats):
        print(f"{Fore.GREEN}Stats updated in README.")
    else:
        print(f"{Fore.YELLOW}Stats already up to date in README. [No changes made]")


def main(args: list[str] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Update stats in the README file",
        epilog="Example: `python3 -m aoc_utils_runarmod updateStats`",
        prog="aoc_utils_runarmod updateStats",
    )
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    update_stats()


if __name__ == "__main__":
    main()
