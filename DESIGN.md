# stonks Design

## Summary

Minimal design report.

## Architecture

    input ---> retrieval ---> processing ---> report ---> output
                                  ^
                                  | 
                                  v
                               database

## Components

### Input

User input is provided via an array of company objects in JavaScript Object Notation (JSON) format, stored in the `input` directory. Various assumptions are stored in `assumptions.toml`. Other settings relating to the operation of the program will be stored in a `settings.toml`.

### Retrieval

Acquires financial market data from various API endpoints.

### Yahoo Finance API

Request financial data from the [Yahoo Finance API](https://rapidapi.com/sparior/api/yahoo-finance15).

### Processing

#### Valuation Metrics

Calculates various metrics to be used to value the company.

#### Valuation Models

##### Discounted Cash Flow

Implements a value investing staple; a [Discounted Cash Flow](https://www.investopedia.com/terms/d/dcf.asp) tool.

#### Intrinsic Value

Computes the [Intrinsic Value](https://www.investopedia.com/terms/i/intrinsicvalue.asp) of a company.

### Database

Stores computed data of interest, to keep a historical log of promising valuations.

PostgreSQL or MySQL are the candidate database technologies. 

### Report

Builds a report for each analysed company.

### Output

Outputs the company report. Candidate output format is HTML5, to be later formatted with Bootstrap.
