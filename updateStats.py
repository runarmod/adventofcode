"""
This script is used to update the stats in the README file.
It downloads the stats from the website and updates the
README file accordingly.
"""
import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from dotenv import load_dotenv

colorama_init(autoreset=True)
load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit(f"{Fore.YELLOW}COOKIE not found in .env")


def update_README(stats: str) -> bool:
    """
    Update the stats in the README file. Returns True
    if the stats were updated. False otherwise.
    """
    update_stats_py_abs_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(update_stats_py_abs_dir, "README.md")

    with open(path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    replacer = r"<!-- START STATS -->(.|\n)*<!-- END STATS -->"
    replacement = f"<!-- START STATS -->\n```py\n{stats}\n```\n<!-- END STATS -->"

    newContent = re.sub(replacer, replacement, readme_content)

    if newContent == readme_content:
        return False

    with open(path, "w", encoding="utf-8") as f:
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
        stars = element.find("span").text
        stats += f"{year} {stars}\n"
    stats = stats.strip()

    total_star_count = soup.find_all("span", {"class": "star-count"})[-1]
    total_star_text = f"\n\nTotal stars: {total_star_count.text}"
    return stats + total_star_text


def main() -> None:
    URL = "https://adventofcode.com/events"
    cookies = {"session": COOKIE}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) "
        + "Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1"
    }
    page = requests.get(URL, cookies=cookies, headers=headers)
    if page.status_code != 200:
        sys.exit(f"{Fore.RED}Could not retrieve stats.\nError: {page.status_code}\n{page.content}")

    stats = get_stats_from_HTML(page)
    if update_README(stats):
        print(f"{Fore.GREEN}Stats updated in README.")
    else:
        print(f"{Fore.YELLOW}Stats already up to date in README. [No changes made]")


if __name__ == "__main__":
    main()
