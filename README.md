# stonks

## Summary

The quantitative analysis component of a [Value Investing](https://www.investopedia.com/terms/v/valueinvesting.asp) approach. See `DESIGN.md` for an overview of the current application design. See `TO DO.md` for a list of features, work items and issues (to be migrated to GitHub).

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

## Requirements

"stonks" requires an installation of python3 (tested on Python 3.11.3).

### Python Install

Instructions on how to set up and install python3.

#### Windows

Download and install the latest version of python3 [here](https://www.python.org/downloads/). Then add the parent directory of `python.exe` and `pip.exe` to the [System Environment Variables `Path` field](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)). Where `<username>` is the name of the windows user account, the default path for `python3.exe` is:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python311\
```

and for `pip.exe` is:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python311\Scripts\
```

#### Linux

python3 comes pre-installed on most modern distributions.

To manually install, execute:

```bash
sudo apt-get install python3.11
```

## Install

### Dependencies

Install project dependencies by running `install.bat`.

To install from a Command Line Interface (CLI):

```bash
pip3 install requirements.txt
```

### Environment Variables

Create a file in the project root directory called `.env`. Acquire the respective API keys for each provider and save them in `.env` under the names, where `<key>` is replaced by your personal access key:

```text
RAPID_API_KEY=<[rapid-api-key](https://docs.rapidapi.com/docs/keys)>
```

## Configuration

The user input file is named `input.json`. All necessary assumptions used for calculations are present in `assumptions.toml`. Application specific settings are in `settings.toml`.

## Usage

Launch the application by running `run.bat`.

To execute from a CLI:

```bash
python main.py
```

## Test

To run unit tests, execute:

```bash
pytest
```

To see the code coverage report, execute:

```bash
coverage report --fail-under=80
```
