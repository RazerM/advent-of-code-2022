# Installation

```bash
git clone https://github.com/RazerM/advent-of-code-2022
cd advent-of-code-2022
python3 -m venv --prompt aoc2022 .venv
source .venv/bin/activate
pip install -e .
```

# CLI

Set the `AOC_SESSION` environment variable to the value of your
https://adventofcode.com `session` cookie. It may also be added to an `.env`
file.

## Manual Commands

```bash
aoc2022 download 1 input/1.txt
```

```bash
aoc2022 run 1 input/1.txt
```

## Automatic Commands

These commands assume an `input` directory is being used. Use `prepare` to
download all available input files and create any missing python modules in
`src/aoc2022` from a template.

```bash
aoc2022 prepare
```

Run the solution for the current day (or provide it as an argument). Uses
the corresponding input file automatically.

```bash
aoc2022 autorun [day]
```
