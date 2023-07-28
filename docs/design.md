# stonks Design

## Table of Contents

- [stonks Design](#stonks-design)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
  - [High-Level Architecture](#high-level-architecture)
  - [Components](#components)
    - [Input](#input)
    - [Configuration](#configuration)
    - [Manager](#manager)
    - [Retrieval](#retrieval)
      - [API Client](#api-client)
      - [Request Builder](#request-builder)
    - [Processing](#processing)
      - [Valuation Metrics](#valuation-metrics)
      - [Valuation Models](#valuation-models)
        - [Discounted Cash Flow](#discounted-cash-flow)
      - [Intrinsic Value](#intrinsic-value)
    - [Storage](#storage)
    - [Report](#report)
    - [Output](#output)

## Summary

Minimal design report.

Diagrams should be converted to UML format, most likely in [LucidChart](https://www.lucidchart.com/pages/product).

## High-Level Architecture

    configuration ---> manager ---> retrieval ---> processing ---> report ---> output
                                           ^        ^
                                           |        | 
                                           v        v
                                            storage

Note that currently `report` component is not implemented as an insufficient amount of data is generated.

## Components

Describes the individual components, sub-packages and modules.

### Input

User input is provided via a collection object containing company objects in JavaScript Object Notation (JSON) format, stored in the `input` directory. Various assumptions are stored in `assumptions.toml`. Other settings relating to the operation of the program will be stored in a `settings.toml`.

### Configuration

Responsible for configuring the application by acquiring `ApplicationSettings` from `settings.toml`, `MetricAssumptions` from `assumptions.toml` and environment variables from (you guessed it) the environment. Attributes of `ApplicationSettings` and `MetricAssumptions` are provided directly to dependent components.

Currently environment variables are set as direct attributes of an `ApplicationSettings` instance. Consider maintaining separation between environment variables and application settings to isolate issues. Settings acquired from `settings.toml` are effectively hard-coded with each version of the application making issues associated with them easily reproducible, whereas environment variables are secret.

Consider making `ApplicationSettings` and `MetricAssumptions` [singleton](https://refactoring.guru/design-patterns/singleton) classes.

### Manager

`ApplicationManager` is responsible for managing the operation of the application. `ApplicationManager` is instantiated with an `ApplicationSettings` instance assigned as `ApplicationManager.settings` and shall (in future) also require a `MetricAssumptions` instance assigned `ApplicationManager.assumptions`.

### Retrieval

Responsible for data acquisition and packaging.

#### API Client

`APIClient` is responsible for instantiating `requests.Session` objects.

Must decide if API tokens shall be scoped to  `APIClient` or `Session`.

#### Request Builder

`RequestBuilder` shall be the base class for all concrete request [factories](https://refactoring.guru/design-patterns/factory-method) which shall be responsible for instantiating concrete `Request` objects derived from `requests.Request` and subsequently `stonks.retrieval.`.

An API key is passed to the request builder, acquired from `ApplicationSettings`

          RequestBuilder              request.Request
                |                           |
                v                           v
      RapidAPIRequestBuilder   --->   RapidAPIRequest
                |                           |
                v                           v
    YahooFinanceRequestBuilder ---> YahooFinanceRequest

See [Yahoo Finance API](https://rapidapi.com/sparior/api/yahoo-finance15).

### Processing

`Processing` takes data acquired by `retrieval.APIClient` and computes metrics from various models to be compiled and reported.

#### Valuation Metrics

Calculates various metrics to be used to value the company.

#### Valuation Models

Implementation of different techniques for valuing companies.

##### Discounted Cash Flow

Implements a value investing staple; a [Discounted Cash Flow](https://www.investopedia.com/terms/d/dcf.asp) tool.

#### Intrinsic Value

Computes the [Intrinsic Value](https://www.investopedia.com/terms/i/intrinsicvalue.asp) of a company.

### Storage

Stores requested and computed data of interest in JSON format, to keep a historical log of promising valuations.

PostgreSQL or MySQL are the candidate database technologies.

### Report

Builds a report for each analysed company that matches eligibility criteria.

### Output

Outputs company reports. Candidate output format is HTML5, to be later formatted with Bootstrap in order to facilitate web front-end integration.
