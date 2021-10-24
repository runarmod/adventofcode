import os, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from cookie import cookie
import pytz
import webbrowser


# Get input either in command line or input
if len(sys.argv) != 3:
    year = input("Please enter a year: ")
    day = input("Please enter a day: ")
else:
    year = str(sys.argv[1])
    day = str(sys.argv[2])

try:
    int(day)
    int(year)
except:
    raise Exception("Day and/or year is not number")

if int(day) > 25 or int(day) < 1:
    raise Exception("Day must be between 1 and 25")

if int(year) > datetime.now().year or int(year) < 2015:
    raise Exception("Year must be between 2015 and %i" %datetime.now().year)


# Find how long until
now = datetime.now(tz=pytz.timezone('EST'))
release = now.replace(year = int(year), month = 12, day = int(day), hour = 0, minute = 0, second = 0, microsecond = 0)
if now < release:
    raise Exception("The problem doesn't exist yet.\nTime remaining: " + str(release - now))


# Make new year directory if it doesn't exist
path = "." + "\\" + year
try:
    os.mkdir(path)
except OSError:
    pass

path += "\\" + day

if os.path.isdir(path):
    raise Exception("Day already exists.\nQuiting...\n")

# Create folder from input
try:
    os.mkdir(path)
except OSError:
    raise Exception("Creation of the directory %s failed" % path)


# Crate testinput file
open(path + "/testinput.txt", 'w').close()


URL = "https://adventofcode.com/" + year + "/day/" + day
# Make inputfile
with open(path + "/input.txt", "w") as f:
    cookies = {'session': cookie}
    inputURL = URL + "/input"
    page = requests.get(inputURL, cookies=cookies)
    soup = BeautifulSoup(page.content, "html.parser")
    f.write(soup.contents[0])

# Create part 1 and 2
part1 = path + "/part1.py"
for i in range(2):
    with open(path + "/part" + str(i + 1) + ".py", "w") as f:
        with open("template.py", "r") as template:
            f.write(template.read())

# Success!
print(str(path) + " and adjacent files created!")
if input("Open VS Code? (y/n) ") == "y":
    print("Opening VS Code!")
    os.system("code " + path)
if input("Open challenge? (y/n) ") == "y":
    print("Opening challenge!")
    webbrowser.open(URL)