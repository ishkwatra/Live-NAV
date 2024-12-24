import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'VA Tech Wabag Limited': {'symbol': 'WABAG', 'weight': 0.0422},
    # add more
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'VA Tech Wabag Limited': {'symbol': 'WABAG', 'weight': 0.0422},
    # add more
}

# Fetch current and previous day price of all stocks in portfolio


def fetch_stock_price(symbol):
    # Set the correct URL of the stock quote page
    url = f'https://finance.yahoo.com/quote/{symbol}.NS/'
    # Define headers to simulate a real browser request (avoiding being blocked)
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Make the HTTP request to the page
    response = requests.get(url, headers=headers)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetch current price, return -1 if no price found
    current_price_element = soup.find(
        'fin-streamer', {'data-field': 'regularMarketPrice'})
    current_price = float(current_price_element.text.replace(
        ',', '')) if current_price_element else -1

    # Fetch previous close price, return -1 if no price found
    prev_close_element = soup.find(
        'fin-streamer', {'data-field': 'regularMarketPreviousClose'})
    previous_close = float(prev_close_element.text.replace(
        ',', '')) if prev_close_element else -1

    return current_price, previous_close

# estimate nav change by calculating percentage change for each stock and multiplying it with its weightage


def estimate_nav_change(portfolio):

    total_change = 0

    # count errors for all -1 received, and count serial number of stocks
    errors = 0
    calc_weight = 0
    stock_num = 1
    for stock, data in portfolio.items():
        symbol = data['symbol']
        weight = data['weight']

        prices = fetch_stock_price(symbol)
        current_price = prices[0]
        previous_close = prices[1]

        if current_price == -1 or previous_close == -1:
            print(
                f"Stock {stock_num} - Error faced! Excluded from calculation.")
            errors += 1
            stock_num += 1
            time.sleep(.5)  # To prevent overwhelming the server
            continue

        print(f"Stock {stock_num} -", symbol, "; Prev - ₹",
              previous_close, "; Curr - ₹", current_price)

        price_change = (current_price - previous_close) / previous_close
        weighted_change = weight * price_change
        total_change += weighted_change
        calc_weight += weight

        stock_num += 1
        time.sleep(.5)  # To prevent overwhelming the server

    # print success rate
    print()
    print(f"Errors faced - {errors}")
    print(
        f"Stocks Calculated - {len(portfolio)-errors}/{43} ({(calc_weight*100):.2f}% out of 93.13%)")
    print("Debt - 0%")
    print("Others (Cash, etc.) - 6.87%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 23-12-2024")
    return total_change

# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/motilal-oswal-small-cap-fund-direct-plan-growth/MMOA011"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    nav_element = soup.find('span', class_='amt')
    if nav_element is None:
        return -1
    prev_nav = float((nav_element.text.strip())[2:])
    return prev_nav

# main:


# fetch current nav
previous_nav = fetch_previous_nav()

# calc change
print("\nChoose depth:")
print("1. Nominal Analysis (Fast: 15-20s)")
print("2. In-Depth Analysis (Slow: 90-95s)")
str = input("Enter: ")
print()
if str == "1":
    nav_change = estimate_nav_change(portfolio1)
else:
    nav_change = estimate_nav_change(portfolio2)
estimated_nav = previous_nav * (1 + nav_change)

# today's date
today_date = datetime.now().strftime('%d-%m-%Y')
yesterday_date = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')

# print the change
print()
print(f'Previous NAV {yesterday_date}: ₹{previous_nav:.4f}')
print(f'Estimated NAV {today_date}: ₹{estimated_nav:.4f}')

# calc profit
tot_investment = 2000  # Enter Manually
tot_units = 0.977  # Enter Manually
current_amt = tot_units*estimated_nav
profit = current_amt - tot_investment

# print profits
print()
print(f'Invested Amount: ₹{tot_investment:.4f}')
print(f'Current Amount: ₹{current_amt:.4f}')
