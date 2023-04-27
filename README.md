# Advent of Code

This repository contains of all of my code from [advent of code](https://adventofcode.com/). Most is undone, and will get updated as I complete more.

This repository contains a setup file, which will initiate a work-directory with a template, in addition to downloading the input using a cookie found in [.env](https://github.com/runarmod/adventofcode/blob/main/.env.example).

Years completed:

- [x] 2015
- [ ] 2016
- [ ] 2017
- [ ] 2018
- [ ] 2019
- [ ] 2020
- [ ] 2021
- [ ] 2022

## Installation

Clone the directory, install dependencies, and copy the .env file. Make sure to fill in the advent of code cookie in the .env file.

```
git clone https://github.com/runarmod/adventofcode.git
cd adventofcode
pip3 install -r requirements.txt
cp .env.example .env
```

## Usage

Delete directories 2015-2022 if you want to start from scratch.

Create a work-directory for december 1st 2015, download the input file, and open the directory in vs-code.

```
python3 setup.py -y 2015 -d 1 -c
```

Create a work-directory for today, open the directory in vs-code and wait for the release to download the input file and open the problem in the browser.

```
python3 setup.py -twcb
```

Force download the input file for today.

```
python3 setup.py -if
```

Force creation of a work-directory for december 24th 2021. This will overwrite any existing directory and files.

```
python3 setup.py -f -y 2021 -d 24
```
