import os

import pyperclip
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from markdownify import markdownify

from .config import get_cookie
from .updateStats import update_stats

colorama_init()


def request_submit(
    year: int | str,
    day: int | str,
    part1: str | None,
    part2: str | None,
) -> None:
    """
    Request to submit the answer to the Advent of Code website.
    This function will decide whether to submit part 1, part 2 or neither.
    Year and day must be numbers.
    """

    if isinstance(year, str) and year.isdigit():
        year = int(year)

    if isinstance(day, str) and day.isdigit():
        day = int(day)

    if not isinstance(year, int) or not isinstance(day, int):
        raise TypeError("Year and day must be numbers.")

    URL = f"https://adventofcode.com/{year}/day/{day}/answer"

    if part2:
        submit(day, 2, part2, URL)
    elif part1:
        correct_part1 = submit(day, 1, part1, URL)
        if correct_part1 and day == 25:
            submit(day, 2, "0", URL)
    else:
        print(f"{Fore.YELLOW}No answer generated.")


def submit(day: int, part: int, answer: str, url: str) -> bool:
    """
    Submit the answer to the Advent of Code website, and print the response.
    Return True if the answer was correct, False otherwise.
    """
    COOKIE = get_cookie()
    question = f"Answer for part {part} ({answer}) generated. Send? (y/[n]) "
    if day != 25 or part == 1:
        if input(question).lower() not in ("y", "ye", "yes"):
            print(f"{Fore.YELLOW}Did not submit.")
            return

    data = {"level": str(part), "answer": answer}
    response = requests.post(url, data=data, cookies={"session": COOKIE})

    if response.status_code != 200:
        print(f"{Fore.RED}Error: {response.status_code}\n{response.content}")
        return False

    soup = BeautifulSoup(response.content, "html.parser")
    childsoup = soup.find("article")
    readable_response = markdownify(str(childsoup), heading_style="ATX").strip()

    if (
        "That's the right answer!" in readable_response
        or "Congratulations!" in readable_response
    ):
        print(f"{Fore.GREEN}Correct!")
        if not (day == 25 and part == 1):
            update_stats()
        return True

    print(f"{Fore.RED}{readable_response}")
    return False


def write_solution(path: str, part1_text: str, part2_text: str) -> None:
    """
    Write the solution to the solution.txt file.
    """
    with open(os.path.join(path, "solution.txt"), "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1: str | int | None, part2: str | int | None):
    """
    Copy the most relevant answer (part 1 or 2) to the clipboard, or neither.
    """
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)
