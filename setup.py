# This program is will create the needed files for
# a problem and get the input it may also open the
# problem in the browser and start a vs code session
import argparse
import contextlib
import os
import sys
import webbrowser
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init as colorama_init
from dotenv import load_dotenv
from markdownify import markdownify as md

from utils import countdown

colorama_init(autoreset=True)
load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit(f"{Fore.YELLOW}COOKIE not found in .env")


def main():
    def updateNow():
        global now
        now = datetime.now(tz=pytz.timezone("EST"))

    updateNow()
    parser = argparse.ArgumentParser(
        description="AOC setup and download. If neither day nor year is supplied, "
        + "today's day will be used.",
        epilog="Example: `python3 setup.py -d 13 -y 2018 -cb`",
    )
    parser.add_argument(
        "-d", help="Day", default=now.day, choices=range(1, 25 + 1), type=int
    )
    parser.add_argument(
        "-y", help="Year", default=now.year, choices=range(2015, now.year + 1), type=int
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t", help="Today", action="store_true", default=False, dest="today"
    )
    group.add_argument(
        "-w",
        "--wait",
        action="store_true",
        help="Create template, wait for puzzle to be released, and download it.",
    )
    parser.add_argument("-i", action="store_true", help="Only download input.")
    parser.add_argument("-b", action="store_true", help="Open browser.")
    parser.add_argument("-c", action="store_true", help="Open VS code.")
    parser.add_argument(
        "-f",
        action="store_true",
        help="Force download and file-creation even when they exist. DANGEROUS!",
    )

    args = parser.parse_args()
    if args.today:
        args.d = now.day
        args.y = now.year

    if args.wait:
        args.d = now.day + 1
        args.y = now.year

    # Find how long until
    release = now.replace(
        year=args.y, month=12, day=args.d, hour=0, minute=0, second=0, microsecond=0
    )

    if now < release and not args.wait:
        sys.exit(
            f"{Fore.RED}The problem doesn't exist yet.\n"
            + f"Time remaining: {str(release - now)}\n"
            + "Use wait flag to wait for release."
        )

    if args.wait and (release - now).total_seconds() > 60 * 60:
        sys.exit(
            f"{Fore.YELLOW}Not waiting more than an hour... Quiting...\n"
            + f"Time remaining: {release - now}"
        )

    # Make new year directory if it doesn't exist
    setupPyAbsDir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(setupPyAbsDir, str(args.y))
    with contextlib.suppress(OSError):
        os.mkdir(path)

    # Make new day directory if it doesn't exist
    path = os.path.join(path, str(args.d).zfill(2))
    with contextlib.suppress(OSError):
        os.mkdir(path)

    if not args.i:
        # Crate testinput file
        if (
            not os.path.exists(testPath := os.path.join(path, "testinput.txt"))
            or args.f
        ):
            open(testPath, "w").close()

        # Create part 1 and 2
        if not os.path.exists(mainPath := os.path.join(path, "main.py")) or args.f:
            with open(mainPath, "w") as f:
                with open(os.path.join(setupPyAbsDir, "template.py"), "r") as template:
                    f.write(
                        template.read()
                        .replace('"CHANGE_YEAR"', str(args.y))
                        .replace('"CHANGE_DATE"', str(args.d))
                    )

        # Create URL file
        if not os.path.exists(urlPath := os.path.join(path, "problem.url")) or args.f:
            with open(urlPath, "w") as f:
                f.write(
                    f"[InternetShortcut]\nURL=https://adventofcode.com/{args.y}/day/{args.d}\n"
                )

    URL = f"https://adventofcode.com/{args.y}/day/{args.d}"

    # Open VS Code
    if args.c:
        print(f"{Fore.GREEN}Opening VS Code!")
        os.system(f"code {path}")

    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1"

    # Make inputfile
    if not os.path.exists(inputPath := os.path.join(path, "input.txt")) or args.f:
        if args.wait:
            # Wait for puzzle to be released
            updateNow()
            if not countdown(release):
                sys.exit(f"{Fore.RED}Countdown failed. Quiting...")

        cookies = {"session": COOKIE}
        inputURL = f"{URL}/input"
        headers = {"User-Agent": USER_AGENT}
        page = requests.get(inputURL, cookies=cookies, headers=headers)
        if page.status_code != 200:
            sys.exit(
                f"{Fore.RED}Input download failed\nError: {page.status_code}\n{page.content}"
            )

        with open(inputPath, "w") as f:
            f.write(page.content.decode())
        print(f"{Fore.GREEN}Input downloaded to {inputPath}")
    else:
        print(f"{Fore.YELLOW}Inputfile already exists. Continuing...")

    if not os.path.exists(taskPath := os.path.join(path, "task.md")) or args.f:
        cookies = {"session": COOKIE}
        taskURL = f"{URL}"
        headers = {"User-Agent": USER_AGENT}
        page = requests.get(taskURL, cookies=cookies, headers=headers)

        if page.status_code != 200:
            sys.exit(
                f"{Fore.RED}Task download failed\nError: {page.status_code}\n{page.content}"
            )

        soup = BeautifulSoup(page.content, "html.parser")
        childsoup = soup.find("article")
        with open(taskPath, "w") as f:
            f.write(md(str(childsoup), heading_style="ATX"))
        print(f"{Fore.GREEN}Task downloaded to {taskPath}")

    # Open browser
    if args.b:
        print(f"{Fore.GREEN}Opening challenge!")
        webbrowser.open(URL)


if __name__ == "__main__":
    main()
