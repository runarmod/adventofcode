# Advent of Code

[![wakatime](https://wakatime.com/badge/user/4196dd87-492b-41f6-b435-4745a3d9200d/project/e525481b-ae87-4c3d-8306-fdc04898c825.svg)](https://wakatime.com/badge/user/4196dd87-492b-41f6-b435-4745a3d9200d/project/e525481b-ae87-4c3d-8306-fdc04898c825)

This repository contains of all of my code from [advent of code](https://adventofcode.com/).

The project uses [uv](https://docs.astral.sh/uv/). Run `uv sync` to install the dependencies and the helper package (a uv workspace member in `package/`). Use the `config` command to set the needed variables (`uv run aoc-utils config`). There are some utility commands/functions which can be used to download all inputs, update the stars in the README, and sending answers to the aoc website.

## My statistics

<!-- START STATS -->
```py
[2025] 24* / 24*
[2024] 50* / 50*
[2023] 50* / 50*
[2022] 50* / 50*
[2021] 50* / 50*
[2020] 50* / 50*
[2019] 50* / 50*
[2018] 50* / 50*
[2017] 50* / 50*
[2016] 50* / 50*
[2015] 50* / 50*

Total stars: 524*
```
<!-- END STATS -->

## Installation

Clone the directory, install the dependencies, and set the configuration.

```bash
git clone https://github.com/runarmod/adventofcode.git
cd adventofcode
uv sync
uv run aoc-utils config -c <cookie>
uv run aoc-utils config -r <repo>
uv run aoc-utils config -t <template>
```

## Usage

Delete all the year directories (2015 and later) if you want to start from scratch.

Create a work-directory for december 1st 2015, download the input file, and open the directory in vs-code.

```bash
uv run aoc-utils start -y 2015 -d 1 -c
```

Create a work-directory for tomorrow, open the directory in vs-code and wait for the release to download the input file and open the problem in the browser.

```bash
uv run aoc-utils start -wcb
```

Force download the input file for today.

```bash
uv run aoc-utils start -if
```

Force creation of a work-directory for december 24th 2021. This will overwrite any existing directory and files.

```bash
uv run aoc-utils start -f -y 2021 -d 24
```

Update the stars in the README.

```bash
uv run aoc-utils updateStats
```
