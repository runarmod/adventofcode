import os
import re
from datetime import datetime, timedelta

import pyperclip
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from markdownify import markdownify

from .config import get_cookie, get_repo_path
from .db import (
    SubmissionStatus,
    get_input,
    insert_correct_submission,
    insert_failed_submission,
    insert_input,
    save_code_snapshot,
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

    valid, msg, already_correct = validate_submission(year, day, part, submission)
    if part == 1 and already_correct:
        print(f"{Fore.YELLOW}Part 1 is already correct. Interpreting as part 2.")
        part = 2
        submission = part2
        valid, msg, _ = validate_submission(year, day, part, submission)

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
            save_code_snapshot(year, day, part)
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
        time_str = match.group(1)
        hour_min = re.match(r"(?:(\d+)m )?(\d+)s", time_str)
        if not hour_min:
            print(
                f"{Fore.RED}Timeout: {time_str}.\n(This is an unexpected timeout format, please contact the developer)"
            )
            return SubmissionStatus.ERROR
        minutes, seconds = hour_min.groups()
        minutes = int(minutes) if minutes is not None else 0
        seconds = int(seconds) if seconds is not None else 0

        print(f"{Fore.RED}Timeout: {time_str} left")
        now = datetime.now()
        future = now + timedelta(minutes=minutes, seconds=seconds)
        print(f"{Fore.BLUE}Try again at {future.strftime('%H:%M:%S')}")

        return SubmissionStatus.ERROR

    if "You don't seem to be solving the right level" in readable_response:
        print(
            f"{Fore.RED}You don't seem to be solving the right level. Did you already complete it?"
        )
        return SubmissionStatus.ERROR

    if match := re.search(
        r"Please wait ([\w\s]+) before trying again", readable_response, re.IGNORECASE
    ):
        time_str = match.group(1)
        match = re.match(r"(\d+|one|five|fifteen) minutes?", time_str)
        print(f"{Fore.RED}Timeout: {time_str}")
        if not match:
            print(
                f"{Fore.RED}(This is an unexpected timeout format, please contact the developer)"
            )
        else:
            minutes = match.group(1)
            match minutes:
                case "one":
                    minutes = 1
                case "five":
                    minutes = 5
                case "fifteen":
                    minutes = 15
                case _:
                    minutes = int(minutes)
            now = datetime.now()
            future = now + timedelta(minutes=minutes)
            print(f"{Fore.BLUE}Try again at {future.strftime('%H:%M:%S')}")
        # Don't return an error status, as we might get more information (e.g. too high/low)

    if "too low" in readable_response.lower():
        print(f"{Fore.RED}Too low.")
        return SubmissionStatus.TOO_LOW

    if "too high" in readable_response.lower():
        print(f"{Fore.RED}Too high.")
        return SubmissionStatus.TOO_HIGH

    if "not the right answer" in readable_response.lower():
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


def get_data(year: int, day: int):
    """
    Get the input data for a given year and day.
    Reads the file in the cache, if it exists.
    If neither the file in the repo nor the data is in the cache, it will download the data.
    """
    REPO_PATH = get_repo_path()
    input_file_path = os.path.join(REPO_PATH, str(year), str(day).zfill(2), "input.txt")
    if os.path.exists(input_file_path):
        with open(input_file_path, "r") as f:
            return f.read()

    try:
        data = get_input(year, day)
    except KeyError:
        URL = f"https://adventofcode.com/{year}/day/{day}"
        cookies = {"session": get_cookie()}
        inputURL = f"{URL}/input"
        headers = {
            "User-Agent": "github.com/runarmod/adventofcode by runarmod@gmail.com"
        }
        page = requests.get(inputURL, cookies=cookies, headers=headers)
        if page.status_code != 200:
            raise Exception(
                f"Input download failed\nError: {page.status_code}\n{page.content}"
            )
        data = page.text
        insert_input(year, day, data)

    with open(input_file_path, "w") as f:
        f.write(data)
    return data
