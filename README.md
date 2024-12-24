# Live-NAV

_**README: Mutual Fund NAV Estimation Tool**_
**Project Overview:**
This project is a Python-based Mutual Fund NAV Estimation Tool that provides an approximate estimate of the current day's NAV (Net Asset Value) for mutual funds. NAVs are officially calculated by fund houses at the end of each trading day but are only published the following day. This tool bridges the gap by providing a real-time estimate using the current market performance of the fund's holdings.

**Key Features:**
1. Two Levels of Analysis:
  i. Nominal Analysis: For quick estimation using a summarized portfolio (~15-20 seconds).
  ii. In-Depth Analysis: For a comprehensive estimate using a detailed portfolio (~120-130 seconds).

2. Dynamic Stock Price Fetching:
  i. Automatically retrieves real-time stock prices (current and previous closeing price) using Yahoo Finance for each stock in the portfolio.

3. Accurate Weightage Calculations:
   i. Tracks and calculates the weightage of stocks successfully fetched.
   ii. Reports errors for stocks that fail to fetch prices and excludes them from calculations.

4. NAV Estimation:
   i. Calculates the percentage change for each stock.
   ii. Multiplies the percentage change by its weightage to estimate the fund's total NAV change.

5. Previous NAV Fetching:
   i. Retrieves the most recent NAV from Moneycontrol.
   ii. Equity-Cash-Debt Breakup: Provides insights into the fund's asset allocation, including equity, cash, and debt percentages.

6. Investment Tracking:
   i. Accepts user input for total investment amount and units held. (in-progress)
   ii. Calculates the current value of the investment and overall profit/loss based on the estimated NAV. (in-progress)

**How It Works:**
1. Calculation Logic:
Multiply the percentage change of each stock by its weight in the portfolio.
Sum up these weighted changes to get the overall portfolio change percentage.
Formulas:
Estimated NAV Change = ∑ (Weight of Stock × Percentage Change)
Estimated NAV = Previous NAV × (1 + Estimated NAV Change)

2. Output:
Displays errors and success rates for stock data retrieval.
Shows previous and estimated NAV, investment value, and profit/loss.

3. Requirements:
i. Python 3.6+
ii. Libraries: requests, beautifulsoup4

**Future Enhancements:**
1. Code Optimization:
Use multi-threading for faster stock price fetching.
Add retry logic for failed requests and implement logging for debugging.

2. Data Source Improvements:
Integrate backup data sources or alternatives to Yahoo Finance.
Allow portfolio storage in CSV or databases instead of hardcoding.

3. Usability Enhancements:
Create a user-friendly interface (e.g., GUI with tkinter or web app using Flask/Streamlit).
Enable portfolio uploads via CSV and generate detailed reports in CSV, JSON, or PDF formats.

4. New Features:
Fetch and display historical NAV trends.
Include dividend adjustments in NAV calculations.
Add a portfolio comparison feature.

5. Deployment:
Convert the tool into a REST API or web app for remote use.
Deploy on platforms like Heroku or Streamlit Cloud.

6. Code Refactoring and Testing:
Modularize functions for better readability and maintainability.
Add automated tests using unittest or pytest.

7. Add more funds:
Increase the number of mutual funds in our data base.

**Limitations:**
Approximation Only: The estimated NAV may differ from the official NAV due to rounding errors and other holdings of the fund in Cash, Debt, etc. NAV estimates can not consider forex changes (for international funds) and unlisted instruments. Also, some bonds and derivatives in the portfolio need special handling for pricing, which is currently not possible.
API Limitations: Occasional failures in stock price fetching due to server issues or rate limits.

**Contributing:**
Feel free to open issues or submit pull requests for improvements.

