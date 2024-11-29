import os
import re

import pyperclip
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from markdownify import markdownify

from .config import get_cookie
from .db import (
    SubmissionStatus,
    insert_correct_submission,
    insert_failed_submission,
    validate_submission,
)
from .updateStats import update_stats

colorama_init()


def request_submit(
    year: int,
    day: int,
    part1: int | str | None,
    part2: int | str | None,
) -> None:
    """
    Request to submit the answer to the Advent of Code website.
    This function will decide whether to submit part 1, part 2 or neither.
    Year and day must be numbers.
    """
    part = 2 if part2 else 1 if part1 else 0
    if part == 0:
        print(f"{Fore.YELLOW}No answer generated.")
        return

    submission = part2 if part == 2 else part1

    valid, msg = validate_submission(year, day, part, submission)
    if not valid:
        print(f"{Fore.RED}{msg}")
        return

    status = submit(year, day, part, submission)
    match status:
        case SubmissionStatus.NO_ANSWER | SubmissionStatus.ERROR:
            return
        case SubmissionStatus.ALREADY_GUESSED:
            print(f"{Fore.YELLOW}Already guessed.")
            return
        case SubmissionStatus.CORRECT:
            if part == 1 and day == 25:
                submit(year, day, 2, "0")
            insert_correct_submission(year, day, part, submission)
        case (
            SubmissionStatus.INCORRECT
            | SubmissionStatus.TOO_HIGH
            | SubmissionStatus.TOO_LOW
        ):
            insert_failed_submission(year, day, part, submission, status)


def submit(year: int, day: int, part: int, answer: int | str):
    """
    Submit the answer to the Advent of Code website, and print the response.
    Return a status code.
    """
    URL = f"https://adventofcode.com/{year}/day/{day}/answer"
    COOKIE = get_cookie()
    question = f"Answer for part {part} ({answer}) generated. Send? (y/[n]) "
    if day != 25 or part == 1:
        if input(question).lower() not in ("y", "ye", "yes"):
            print(f"{Fore.YELLOW}Did not submit.")
            return SubmissionStatus.NO_ANSWER

    data = {"level": str(part), "answer": str(answer)}
    response = requests.post(URL, data=data, cookies={"session": COOKIE})

    if response.status_code != 200:
        print(f"{Fore.RED}Error: {response.status_code}\n{response.content}")
        return SubmissionStatus.ERROR

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
        return SubmissionStatus.CORRECT

    if match := re.search(r"You have ([\w\d\s]+) left to wait", readable_response):
        print(f"{Fore.RED}Timeout: {match.group(1)} left")
        return SubmissionStatus.ERROR

    if "You don't seem to be solving the right level" in readable_response:
        print(
            f"{Fore.RED}You don't seem to be solving the right level. Did you already complete it?"
        )
        return SubmissionStatus.ERROR

    if match := re.search(
        r"Please wait ([\w\s]+) before trying again", readable_response, re.IGNORECASE
    ):
        print(f"{Fore.RED}Timeout: {match.group(1)}")

    if "too low" in readable_response.lower():
        print(f"{Fore.RED}Too low.")
        return SubmissionStatus.TOO_LOW

    if "too high" in readable_response.lower():
        print(f"{Fore.RED}Too high.")
        return SubmissionStatus.TOO_HIGH

    if "That's not the right answer" in readable_response:
        print(f"{Fore.RED}Incorrect.")
        return SubmissionStatus.INCORRECT

    print(f"{Fore.RED}{readable_response}")
    return SubmissionStatus.ERROR


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
