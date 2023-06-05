# stonks

## Summary

The quantitative analysis component of a [Value Investing](https://www.investopedia.com/terms/v/valueinvesting.asp) approach. See `DESIGN.md` for an overview of the current application design.

## Objectives

### Plan

Scrape company financial data to pick out the most undervalued publicly traded companies. Use the resulting shortlist to perform (manual) qualitative analysis on the best prospects.

1. Retrieve company financial data from various APIs.
2. Process the financial data to compute derived metrics.
3. Process the financial data and derived metrics to produce valuation metrics.
4. Calculate an intrinsic value for the company with assumed metrics as variables. (current intrinsic value)
5. Employ valuation models to predict time-evolution of company valuation with assumed metrics as variables (growth, future intrinsic value).
6. Build a report based on the valuation.
7. Produce valuation reports for all publicly listed companies and filter out the best.
8. After qualitative analysis, select a list of stocks for the watch-list.
9. Perform current market research (including sentiment analysis?) to assess the market outlook on watch-list companies.
10. Buy companies according to the highly scientific "Buy Matrix".

### Buy Matrix

The tricky part here is drawing the lines between undervalued and very undervalued...

|                  | Undervalued | Very undervalued |
|------------------|-------------|------------------|
| Poor Outlook     | NEUTRAL     | BUY              |
| Neutral Outlook  | BUY         | STRONG BUY       |
| Positive Outlook | STRONG BUY  | BARGAIN          |

### Future

If it actually works, slap a WebUI on it and sell (tiers?) of subscription service.

## Requirements Installation

"stonks" requires an installation of python3.11 (tested on Python 3.11.3) and poetry (tested on Poetry 1.5.1).

### Python Installation

Instructions on how to set up and install python3.

#### Windows Python Installation

Download and install the python3.11 [here](https://www.python.org/downloads/). Then add the parent directory of `python.exe` and `pip.exe` to the [System Environment Variables `Path` field](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)). Where `<username>` is the name of the Windows user account, the default path for `python3.exe` is:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python311\
```

#### Debian-Based Linux Distribution Installation

`python3` comes pre-installed on most modern distributions.

To manually install `python3.11` execute:

```bash
sudo add-apt-repository -y 'ppa:deadsnakes/ppa'
sudo apt-get install python3.11
```

### Poetry Installation

Instructions for installing poetry for dependency management and packaging.

#### Windows Poetry Installation

To install poetry on Windows open PowerShell and execute:

```PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

#### Linux Installation

To install poetry on Linux execute:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Application Installation

### Dependencies

On Windows the application is installed by doubling clicking on `install.bat` or executing:

```cmd
./install.bat
```

If Windows raises the warning `Windows protected your PC`, select `More info` then `Run anyway`.

To install from a Command Line Interface (CLI) on Windows or Linux, execute:

```bash
poetry install
```

### Environment Variables

Create a file in the project root directory called `.env`. Acquire the respective API keys for each provider and save them in `.env` under the names, where `<key>` is replaced by your personal access key:

```text
RAPIDAPI_KEY=<[rapid-api-key](https://docs.rapidapi.com/docs/keys)>
```

## Configuration

The user input file is named `input.json`. All necessary assumptions used for calculations are present in `assumptions.toml`. Application specific settings are in `settings.toml`.

## Usage

Launch the application by running `run.bat`.

To execute the application from a CLI, first activate a poetry virtual environment by executing:

```shell
poetry shell
```

Then launch the application by executing:

```shell
stonks
```

The poetry shell session is exited by executing:

```shell
deactivate
```

Note that `stonks` can be executed without entering a poetry shell session by prefixing all commands with (where `<command>` is any command stated in `Usage` or `Test`):

```shell
poetry run <command>
```

## Test

To run unit tests from within a poetry shell session execute:

```shell
pytest
```

To see the code coverage report from within a poetry shell session execute:

```bash
coverage run -m pytest test/
coverage report --fail-under=80
```
