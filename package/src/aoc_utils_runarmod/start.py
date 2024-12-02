"""
This program will create the needed files for a day of
advent of code. It will also download the input, along
with opening the problem in the browser and starting a
vs code session. Read more in the README.md file.
"""

import argparse
import contextlib
import datetime
import os
import re
import sys
import webbrowser

import pytz
from colorama import Fore
from colorama import init as colorama_init

from .config import get_repo_path, get_template_path
from .countdown import countdown
from .util import get_data

colorama_init(autoreset=True)


def main(args: list[str] = None):
    now = None

    def updateNow():
        nonlocal now
        now = datetime.datetime.now(tz=pytz.timezone("EST"))

    updateNow()
    parser = argparse.ArgumentParser(
        description="AOC setup and download. If neither day nor year is supplied, "
        + "today's day will be used.",
        epilog="Example: `python3 -m aoc_utils_runarmod start -d 13 -y 2018 -cb`",
        prog="aoc_utils_runarmod start",
    )
    parser.add_argument(
        "-d", help="Day", default=now.day, choices=range(1, 25 + 1), type=int
    )
    parser.add_argument(
        "-y", help="Year", default=now.year, choices=range(2015, now.year + 1), type=int
    )
    parser.add_argument(
        "-u",
        "--url",
        default="",
        type=str,
        dest="url",
        help="Choose day/year by url, e.g. https://adventofcode.com/2020/day/1",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t", help="Today", action="store_true", default=False, dest="today"
    )
    group.add_argument(
        "-w",
        "--wait",
        action="store_true",
        help="Create template, wait for puzzle to be released (next midnight), and download it.",
    )
    parser.add_argument("-i", action="store_true", help="Only download input.")
    parser.add_argument("-b", action="store_true", help="Open browser.")
    parser.add_argument("-c", action="store_true", help="Open VS code.")
    parser.add_argument(
        "-f",
        action="store_true",
        help="Force download and file-creation even when they exist. DANGEROUS!",
    )

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.today:
        args.d = now.day
        args.y = now.year

    if args.url:
        m = re.match(
            r"https?://adventofcode.com/(?P<year>\d{4})/day/(?P<day>\d{1,2})", args.url
        )
        if not m:
            print(f"{Fore.RED}Invalid url")
            sys.exit(1)
        args.d = int(m.group("day"))
        args.y = int(m.group("year"))

    # Find how long until
    release = now.replace(
        year=args.y, month=12, day=args.d, hour=0, minute=0, second=0, microsecond=0
    )

    if args.wait:
        release = (now + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        if release.month != 12 or release.day not in range(1, 26):
            sys.exit(
                f"{Fore.RED}Can't wait for a day that's not in December. Quiting..."
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

    REPO_PATH = get_repo_path()

    # Make new year directory if it doesn't exist
    path = os.path.join(REPO_PATH, str(release.year))
    with contextlib.suppress(OSError):
        os.mkdir(path)

    # Make new day directory if it doesn't exist
    path = os.path.join(path, str(release.day).zfill(2))
    with contextlib.suppress(OSError):
        os.mkdir(path)

    if not args.i:
        # Create testinput file
        if (
            not os.path.exists(testPath := os.path.join(path, "testinput.txt"))
            or args.f
        ):
            open(testPath, "w").close()

        # Create part 1 and 2
        if not os.path.exists(mainPath := os.path.join(path, "main.py")) or args.f:
            template_path = get_template_path()
            with open(mainPath, "w") as f:
                with open(template_path, "r") as template:
                    f.write(
                        template.read()
                        .replace('"CHANGE_YEAR"', str(release.year))
                        .replace('"CHANGE_DATE"', str(release.day))
                    )

    URL = f"https://adventofcode.com/{release.year}/day/{release.day}"

    # Open VS Code
    if args.c:
        print(f"{Fore.GREEN}Opening VS Code!")
        os.system(f"code {path}")

    # Make inputfile
    if not os.path.exists(inputPath := os.path.join(path, "input.txt")) or args.f:
        if args.wait:
            # Wait for puzzle to be released
            updateNow()
            if not countdown(release):
                sys.exit(f"{Fore.RED}Countdown failed. Quiting...")

        get_data(release.year, release.day)
        print(f"{Fore.GREEN}Input downloaded to {inputPath}")
    else:
        print(f"{Fore.YELLOW}Inputfile already exists. Continuing...")

    # Open browser
    if args.b:
        print(f"{Fore.GREEN}Opening challenge!")
        webbrowser.open(URL)


if __name__ == "__main__":
    main()
