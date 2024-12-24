Building Your Tool
If no existing tool exactly fits your needs, you can build one. Here's how:

Steps to Build a Current-Day NAV Estimation Tool
Data Collection:

Fetch portfolio data for the mutual fund, including stock names and weightages.
Use APIs to fetch the latest stock prices and calculate daily percentage changes.
Calculation Logic:

Multiply the percentage change of each stock by its weight in the portfolio.
Sum up these weighted changes to get the overall portfolio change percentage.
Formula:

Estimated NAV Change
=
∑
(
Weight of Stock
×
Percentage Change
)
Estimated NAV Change=∑(Weight of Stock×Percentage Change)
Then apply:

Estimated NAV
=
Previous NAV
×
(
1
+
Estimated NAV Change
)
Estimated NAV=Previous NAV×(1+Estimated NAV Change)
Interface:

Use Python or JavaScript to create a simple web app or script for inputting the mutual fund and viewing the results.
Platforms like Streamlit (Python) make this easy to deploy.
API Sources:

Alpha Vantage (Free tier available for stock prices).
IEX Cloud (More robust but may require paid plans).
Yahoo Finance (Unofficial APIs or scrapers).
Automate:

Set up the tool to run daily post-market hours for updates.
Approximation Considerations
NAV estimates will not consider intraday variations, forex changes (for international funds), or unlisted instruments.
Some bonds and derivatives in the portfolio may need special handling for pricing.
