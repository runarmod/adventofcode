import os
import sys

import pyperclip
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md

load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit("COOKIE not found in .env")


def request_submit(year, day, part1, part2):
    # Send a POST request to the Advent of Code website
    url = f"https://adventofcode.com/{year}/day/{day}/answer"

    if part2:
        submit(2, part2, url)
    elif part1:
        submit(1, part1, url)
    else:
        print("No answer generated.")


def submit(part, answer, url):
    data = {"level": str(part), "answer": str(answer)}
    if (
        input(f"Answer for part {part} ({answer}) generated. Send? (y/[n]) ").lower()
        == "y"
    ):
        response = requests.post(url, data=data, cookies={"session": COOKIE})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            childsoup = soup.find("article")
            print(md(str(childsoup), heading_style="ATX"))
        else:
            print(f"Error: {response.status_code}\n{response.content}")
            print("ERROR!")
    else:
        print("Did not submit.")


def write_solution(path, part1_text, part2_text):
    with open(os.path.join(path, "solution.txt"), "w") as f:
        f.write(f"{part1_text}\n{part2_text}\n")


def copy_answer(part1, part2):
    copy = part1
    if part2:
        copy = part2

    if copy:
        pyperclip.copy(copy)


if __name__ == "__main__":
    # copy_answer("part1", "part2")
    print(COOKIE)
