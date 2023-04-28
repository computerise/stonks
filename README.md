# stonks

# Summary

The quantitative analysis component of a [Value Investing](https://www.investopedia.com/terms/v/valueinvesting.asp)
approach. See `DESIGN.md` for an overview of the current application design. See `TO DO.md` for a list of features, work
items and issues.

# Objectives

 Scrape company financial data to pick out the most undervalued publicly traded companies. Use the resulting shortlist
 to perform (manual) qualitative analysis on the best prospects.

1. Retrieve company financial data from various APIs.
2. Process the financial data to compute derived metrics.
3. Process the financial data and derived metrics to produce valuation metrics.
4. Calculate an intrinsic value for the company with assumed metrics as variables. (current intrinsic value)
5. Employ valuation models to predict time-evolution of company valuation with assumed metrics as variables (growth,
future intrinsic value).
7. Build a report based on the valuation.
8. Produce valuation reports for all publicly listed companies and filter out the best.
9. After qualitative analysis, select a list of stocks for the watch-list.
10. Perform current market research (including sentiment analysis?) to assess the market outlook on watch-list companies.
11. Buy companies according to the highly scientific "Buy Matrix".

# Buy Matrix

The tricky part here is drawing the lines between undervalued and very undervalued... 

|                  | Undervalued | Very undervalued |
| ---------------- | ----------- | ---------------- |
| Poor Outlook     |   NEUTRAL   |       BUY        |
| Neutral Outlook  |     BUY     |    STRONG BUY    |
| Positive Outlook | STRONG BUY  |     BARGAIN      |

# Future

If it actually works, slap a WebUI on it and sell (tiers?) of subscription service.
