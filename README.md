# stonks

## Table of Contents

- [stonks](#stonks)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
  - [Objectives](#objectives)
    - [Method](#method)
    - [Buy Matrix](#buy-matrix)
    - [Future](#future)
  - [Dependency Installation](#dependency-installation)
    - [Python Installation](#python-installation)
      - [Python Installation on Windows](#python-installation-on-windows)
      - [Python Installation on Debian-Based Linux Distributions](#python-installation-on-debian-based-linux-distributions)
    - [Poetry Installation](#poetry-installation)
      - [Poetry Installation on Windows](#poetry-installation-on-windows)
      - [Poetry Installation on Linux](#poetry-installation-on-linux)
  - [Application Installation](#application-installation)
    - [Dependencies](#dependencies)
    - [Environment Variables](#environment-variables)
  - [Configuration](#configuration)
    - [Settings](#settings)
    - [Assumptions](#assumptions)
  - [Usage](#usage)
    - [Windows Usage](#windows-usage)
    - [Linux Usage](#linux-usage)
  - [Development](#development)
  - [Test](#test)

## Summary

The quantitative analysis component of a [Value Investing](https://www.investopedia.com/terms/v/valueinvesting.asp) approach. See [`docs/design.md`](https://github.com/computerise/stonks/blob/master/docs/design.md) for an overview of the current application design.

## Objectives

### Method

Scrape company financial data to pick out the most undervalued publicly traded companies. Use the resulting shortlist to perform (manual) qualitative analysis on the best prospects.

1. Retrieve company financial data from various APIs.
2. Process the financial data to compute derived metrics.
3. Process the financial data and derived metrics to produce valuation metrics.
4. Calculate an intrinsic value for the company with assumed metrics as variables (current intrinsic value).
5. Employ valuation models to predict time-evolution of company valuation with assumed metrics as variables (growth, future intrinsic value).
6. Build a report based on the valuation and growth forecasts.
7. Produce valuation reports for all publicly listed companies and filter out the best.
8. After qualitative analysis, select a list of stocks for the watch-list.
9. Perform the qualitative analysis component by applying current market research (including sentiment analysis ) to assess the market outlook on watch-list companies.
10. Buy companies according to the highly scientific "Buy Matrix".

### Buy Matrix

The tricky part here is drawing the lines between undervalued and very undervalued...

|                  | Undervalued | Very undervalued |
|------------------|-------------|------------------|
| Poor Outlook     | NEUTRAL     | BUY              |
| Neutral Outlook  | BUY         | STRONG BUY       |
| Positive Outlook | STRONG BUY  | BARGAIN          |

### Future

Once the approach is successful, provide a WebUI (or a REST API) to generate reports in-browser (or provide results via an REST API).

## Dependency Installation

"stonks" requires an installation of python3.11 (tested on Python 3.11.3) and poetry (tested on Poetry 1.5.1).

### Python Installation

Instructions on how to set up and install python3.

#### Python Installation on Windows

Download and install python3.11 [here](https://www.python.org/downloads/). Then add the parent directory of `python.exe` to the [System Environment Variables `Path` field](<https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)>). Where `<username>` is the name of the Windows user account, the default path for `python3.exe` is:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python311\
```

#### Python Installation on Debian-Based Linux Distributions

`python3` comes pre-installed on most modern distributions.

To manually install `python3.11` execute:

```bash
sudo add-apt-repository -y 'ppa:deadsnakes/ppa'
sudo apt-get install python3.11
```

### Poetry Installation

Instructions for installing poetry for dependency management and packaging.

#### Poetry Installation on Windows

To install poetry on Windows open PowerShell and execute:

```PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then add the parent directory of `poetry.exe` to the [System Environment Variables `Path` field](<https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)>). Where `<username>` is the name of the Windows user account, the default path for `poetry.exe` is:

```text
C:\Users\<username>\AppData\Roaming\pypoetry\venv\Scripts\
```

#### Poetry Installation on Linux

To install poetry on Linux execute:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Application Installation

### Dependencies

When using the launcher as prescribed in [Usage](#usage) the application and python dependencies are automatically installed.

To manually install the application from a Command Line Interface (CLI) on Windows or Linux, execute:

```shell
poetry install
```

### Environment Variables

Create a file in the project root directory called `.env`. Acquire the respective API keys for each provider and save them in `.env` under the names (where `<rapid_api_key>` is replaced by your [personal access key for RapidAPI](https://docs.rapidapi.com/docs/keys)):

```text
RAPIDAPI_KEY=<rapid-api-key>
```

## Configuration

### Settings

Settings options related to the general operation of the application are specified in `settings.toml` as a flat object of key-value pairs under `[application]`:

| Key                      | Default Value         | Value Type  | Group   | Description                                                                                                                                 |
|--------------------------|-----------------------|-------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `api_key_names`          | `["RAPIDAPI_KEY"]`    | `list[str]` | Keys    | The environment variable names of API keys.                                                                                                 |
| `outro_duration_seconds` | `5`                   | `float`     | Display | The time delay in seconds before terminating the application after execution.                                                               |
| `log_level`              | `"DEBUG"`             | `str`       | Logs    | The level of log messages displayed in both `stdout` and log files.                                                                         |
| `input_file`             | `"input/s&p500.json"` | `str`       | Paths   | The path to the JSON input file containing company tickers to evaluate.                                                                     |
| `log_directory`          | `"logs/"`             | `str`       | Paths   | The path to the directory where application logs will be generated.                                                                         |
| `storage_directory`      | `"data/s&p500/"`      | `str`       | Paths   | The path to the directory where raw company data will be stored prior to processing (if `store_new_data` is set to `true`).                 |
| `output_directory`       | `"output/"`           | `str`       | Paths   | The path to the directory where candidate companies will be recorded in a JSON output file.                                                 |
| `request_new_data`       | `true`                | `bool`      | Flag    | If `true`, new data will be requested from API endpoints during execution. If `false`, the application will attempt to use stored raw data. |
| `store_new_data`         | `true`                | `bool`      | Flag    | If `true`, newly requested data will overwrite the corresponding stored data. If `false` new data will not be written to raw data files.    |

### Assumptions

Metric Assumptions represent measurable attributes of a market or economy and include interest rates, tax rates, bond rates, rates of return and credit spreads. Currently these are implemented as constants when modelling each company, though estimating the time-evolution of these values should be considered in the future. Default values for these metrics were last collected on 12th June 2023. Metric assumptions are specified in `assumptions.toml` as a nested object of key-value pairs grouped by country, and further grouped by stock market index:

| Key                        | Value Type | Section       | Description                                                                                                                                                                                                                      |
|----------------------------|------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `risk_free_rate_of_return` | `float`    | Country       | The annualised rate of return offered by the country's [short-term (3-month) government bond](https://www.investopedia.com/terms/r/risk-freerate.asp#toc-why-is-the-us-3-month-t-bill-used-as-the-risk-free-rate), as a decimal. |
| `corporate_tax_rate`       | `float`    | Country       | The rate of [corporation tax](https://www.investopedia.com/terms/c/corporatetax.asp) in the country, as a decimal.                                                                                                               |
| `rate_of_return`           | `float`    | Country.Index | The [average annualised rate of return](https://www.investopedia.com/terms/a/aar.asp) of the index, as a decimal.                                                                                                                |
| `average_credit_spread`    | `float`    | Country.Index | The average range between the [lowest and highest rate debt securities](https://www.investopedia.com/terms/c/creditspread.asp) of the index, as a decimal.                                                                       |

## Usage

### Windows Usage

Launch the application on Windows by double-clicking on `LAUNCH_WINDOWS.bat`. If Windows raises the warning `Windows protected your PC`, select `More info` then `Run anyway`.

Launch the application on Linux by executing:

### Linux Usage

```bash
./LAUNCH_LINUX.sh
```

## Development

To manually execute the application from a CLI, first activate a poetry virtual environment by executing:

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

Note that `stonks` can be executed without entering a poetry shell session by prefixing all commands (where `<command>` is any command stated in `Usage` or `Test`) with:

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
