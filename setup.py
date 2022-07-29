# This program is will create the needed files for
# a problem and get the input it may also open the
# problem in the browser and start a vs code session

import argparse
import contextlib
import os
import sys
import requests
from datetime import datetime
from cookie import cookie
import pytz
import webbrowser
import pause


def main():
    def updateNow():
        global now
        now = datetime.now(tz=pytz.timezone("EST"))

    updateNow()
    parser = argparse.ArgumentParser(
        description="AOC setup and download.\n If neither day nor year is supplied, today's day will be used.",
        epilog="Example: setup.py 13 2018",
    )
    parser.add_argument(
        "-d", help="Day", default=now.day + 1, choices=range(1, 25 + 1), type=int
    )
    parser.add_argument(
        "-y", help="Year", default=now.year, choices=range(2015, now.year + 1), type=int
    )
    parser.add_argument(
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

    # Find how long until
    release = now.replace(
        year=args.y, month=12, day=args.d, hour=0, minute=0, second=0, microsecond=0
    )
    if now < release and not args.wait:
        sys.exit(
            f"The problem doesn't exist yet.\nTime remaining: {str(release - now)}\nUse wait flag to wait for release."
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
                    f.write(template.read())

        # Create URL file
        if not os.path.exists(urlPath := os.path.join(path, "problem.url")) or args.f:
            with open(urlPath, "w") as f:
                f.write(
                    f"[InternetShortcut]\nURL=https://adventofcode.com/{args.y}/day/{args.d}\n"
                )

    # Make inputfile
    URL = f"https://adventofcode.com/{args.y}/day/{args.d}"
    if not os.path.exists(inputPath := os.path.join(path, "input.txt")) or args.f:
        if args.wait:
            # Wait for puzzle to be released
            updateNow()
            if (release - now).total_seconds() > 60 * 60 * 24:
                sys.exit(
                    f"Not waiting more than a day... Quiting...\nTime remaining: {release - now}"
                )

            print(f"Waiting for puzzle to be released at {release}")
            pause.until(release)

        with open(inputPath, "w") as f:
            cookies = {"session": cookie}
            inputURL = f"{URL}/input"
            page = requests.get(inputURL, cookies=cookies)
            f.write(page.content.decode())
            print(f"Input downloaded to {inputPath}")
    else:
        print("Inputfile already exists. Continuing...")

    # Success!
    if args.b:
        print("Opening challenge!")
        if os.path.exists(urlFile := os.path.join(path, "problem.url")):
            os.system(urlFile)
        else:
            webbrowser.open(URL)
    if args.c:
        print("Opening VS Code!")
        os.system(f"code {path}")


if __name__ == "__main__":
    main()
