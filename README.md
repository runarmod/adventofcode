# Advent of Code

[![wakatime](https://wakatime.com/badge/user/4196dd87-492b-41f6-b435-4745a3d9200d/project/e525481b-ae87-4c3d-8306-fdc04898c825.svg)](https://wakatime.com/badge/user/4196dd87-492b-41f6-b435-4745a3d9200d/project/e525481b-ae87-4c3d-8306-fdc04898c825)

This repository contains of all of my code from [advent of code](https://adventofcode.com/).

You have to install the package (`pip install package/`) to be able to use the helper functions. Use the `config` command to set the needed variables (`python3 -m aoc_utils_runarmod config`). There are some utility commands/functions which can be used to download all inputs, update the stars in the README, and sending answers to the aoc website.

## My statistics

<!-- START STATS -->
```py
[2024] 26*
[2023] 50*
[2022] 50*
[2021] 50*
[2020] 50*
[2019] 50*
[2018] 50*
[2017] 50*
[2016] 50*
[2015] 50*

Total stars: 476*
```
<!-- END STATS -->

## Installation

Clone the directory, install the package, and set the configuration.

```bash
git clone https://github.com/runarmod/adventofcode.git
cd adventofcode
pip install package/
python3 -m aoc_utils_runarmod config -c <cookie>
python3 -m aoc_utils_runarmod config -r <repo>
python3 -m aoc_utils_runarmod config -t <template>
```

## Usage

Delete directories 2015-2024 if you want to start from scratch.

Create a work-directory for december 1st 2015, download the input file, and open the directory in vs-code.

```bash
python3 -m aoc_utils_runarmod start -y 2015 -d 1 -c
```

Create a work-directory for tomorrow, open the directory in vs-code and wait for the release to download the input file and open the problem in the browser.

```bash
python3 -m aoc_utils_runarmod start -wcb
```

Force download the input file for today.

```bash
python3 -m aoc_utils_runarmod start -if
```

Force creation of a work-directory for december 24th 2021. This will overwrite any existing directory and files.

```bash
python3 -m aoc_utils_runarmod start -f -y 2021 -d 24
```

Update the stars in the README.

```bash
python3 -m aoc_utils_runarmod updateStats
```
