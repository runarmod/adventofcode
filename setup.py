# This program is will create the needed files for
# a problem and get the input it may also open the
# problem in the browser and start a vs code session
import argparse
from bs4 import BeautifulSoup
import contextlib
from countdown import countdown
import http.cookiejar
import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv
import pytz
import webbrowser
import pause
from markdownify import markdownify as md

load_dotenv()
COOKIE = os.getenv("COOKIE")
if COOKIE is None:
    sys.exit("COOKIE not found in .env")


def main():
    def updateNow():
        global now
        now = datetime.now(tz=pytz.timezone("EST"))

    updateNow()
    parser = argparse.ArgumentParser(
        description="AOC setup and download.\n If neither day nor year is supplied, today's day will be used.",
        epilog="Example: setup.py -d 13 -y 2018",
    )
    parser.add_argument(
        "-d", help="Day", default=now.day, choices=range(1, 25 + 1), type=int
    )
    parser.add_argument(
        "-t", help="Today", action="store_true", default=False, dest="today"
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
    if args.today:
        args.d = now.day
        args.y = now.year

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

    # cookies = http.cookiejar.MozillaCookieJar(os.path.join(setupPyAbsDir, "cookies.txt"))
    # cookies.load(os.path.join(setupPyAbsDir, "cookies.txt"), ignore_discard=True, ignore_expires=True)

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
            
            countdown(release)

        with open(inputPath, "w") as f:
            cookies = {"session": COOKIE}
            inputURL = f"{URL}/input"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1'}
            page = requests.get(inputURL, cookies=cookies, headers=headers)
            if page.status_code == 200:
                f.write(page.content.decode())
                print(f"Input downloaded to {inputPath}")
            else:
                sys.exit(
                    f"Input download failed\nError: {page.status_code}\n{page.content}"
                )
    else:
        print("Inputfile already exists. Continuing...")

    if not os.path.exists(taskPath := os.path.join(path, "task.md")) or args.f:
        with open(taskPath, "w") as f:
            cookies = {"session": COOKIE}
            taskURL = f"{URL}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1'}
            page = requests.get(taskURL, cookies=cookies, headers=headers)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                childsoup = soup.find("article")
                f.write(md(str(childsoup), heading_style="ATX"))
                print(f"Task downloaded to {taskPath}")
            else:
                sys.exit(
                    f"Task download failed\nError: {page.status_code}\n{page.content}"
                )
        

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
