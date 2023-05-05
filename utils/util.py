import os
import sys
from typing import Optional, Union

import pyperclip
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from dotenv import load_dotenv
from markdownify import markdownify

from utils.updateStats import update_stats

colorama_init()

load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit(f"{Fore.RED}COOKIE not found in .env")


def request_submit(
    year: Union[int, str], day: Union[int, str], part1: Optional[str], part2: Optional[str]
) -> None:
    """
    Request to submit the answer to the Advent of Code website.
    This function will decide whether to submit part 1, part 2 or neither.
    """

    URL = f"https://adventofcode.com/{year}/day/{day}/answer"

    if part2:
        submit(2, part2, URL)
    elif part1:
        submit(1, part1, URL)
    else:
        print(f"{Fore.YELLOW}No answer generated.")


def submit(part: int, answer: str, url: str) -> None:
    """
    Submit the answer to the Advent of Code website, and print the response.
    """
    question = f"Answer for part {part} ({answer}) generated. Send? (y/[n]) "
    if input(question).lower() not in ("y", "ye", "yes"):
        print(f"{Fore.YELLOW}Did not submit.")
        return

    data = {"level": str(part), "answer": answer}
    response = requests.post(url, data=data, cookies={"session": COOKIE})

    if response.status_code != 200:
        print(f"{Fore.RED}Error: {response.status_code}\n{response.content}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    childsoup = soup.find("article")
    readable_response = markdownify(str(childsoup), heading_style="ATX").strip()
    if "That's the right answer!" in readable_response:
        print(f"{Fore.GREEN}Correct!")
        update_stats()
    else:
        print(f"{Fore.RED}{readable_response}")


def write_solution(path: str, part1_text: str, part2_text: str) -> None:
    """
    Write the solution to the solution.txt file.
    """
    with open(os.path.join(path, "solution.txt"), "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1: Optional[str | int], part2: Optional[str | int]):
    """
    Copy the most relevant answer (part 1 or 2) to the clipboard, or neither.
    """
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)
