import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'Zomato Limited': {'symbol': 'ZOMATO', 'weight': 0.0812},
    'Trent Limited': {'symbol': 'TRENT', 'weight': 0.0647},
    'Kalyan Jewellers India Limited': {'symbol': 'KALYANKJIL', 'weight': 0.0538},
    'Bharti Airtel Limited': {'symbol': 'BHARTIARTL', 'weight': 0.0492},
    'Samvardhana Motherson International Limited': {'symbol': 'MOTHERON', 'weight': 0.0369},
    'Prestige Estates Projects Limited': {'symbol': 'PRESTIGE', 'weight': 0.0360},
    'Coforge Limited': {'symbol': 'COFORGE', 'weight': 0.0355},
    'Apar Industries Limited': {'symbol': 'APARINDS', 'weight': 0.0346},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'Zomato Limited': {'symbol': 'ZOMATO', 'weight': 0.0812},
    'Trent Limited': {'symbol': 'TRENT', 'weight': 0.0647},
    'Kalyan Jewellers India Limited': {'symbol': 'KALYANKJIL', 'weight': 0.0538},
    'Bharti Airtel Limited': {'symbol': 'BHARTIARTL', 'weight': 0.0492},
    'Samvardhana Motherson International Limited': {'symbol': 'MOTHERSON', 'weight': 0.0369},
    'Prestige Estates Projects Limited': {'symbol': 'PRESTIGE', 'weight': 0.0360},
    'Coforge Limited': {'symbol': 'COFORGE', 'weight': 0.0355},
    'Apar Industries Limited': {'symbol': 'APARINDS', 'weight': 0.0346},
    'Suzlon Energy Limited': {'symbol': 'SUZLON', 'weight': 0.0343},
    'Premier Energies Limited': {'symbol': 'PREMIERENE', 'weight': 0.0335},
    'Mankind Pharma Limited': {'symbol': 'MANKIND', 'weight': 0.0335},
    'Gujarat Fluorochemicals Limited': {'symbol': 'FLUOROCHEM', 'weight': 0.0313},
    'HDFC Bank Limited': {'symbol': 'HDFCBANK', 'weight': 0.0299},
    'Bharat Electronics Limited': {'symbol': 'BEL', 'weight': 0.0296},
    'Multi Commodity Exchange of India Limited': {'symbol': 'MCX', 'weight': 0.0295},
    'Inox Wind Limited': {'symbol': 'INOXWIND', 'weight': 0.0295},
    'Amber Enterprises India Limited': {'symbol': 'AMBER', 'weight': 0.0293},
    'The Phoenix Mills Limited': {'symbol': 'PHOENIXLTD', 'weight': 0.0291},
    'Kaynes Technology India Limited': {'symbol': 'KAYNES', 'weight': 0.0282},
    'Hindustan Aeronautics Limited': {'symbol': 'HAL', 'weight': 0.0275},
    'GE Vernova T&D India Limited': {'symbol': 'GVT&D', 'weight': 0.0269},
    'CG Power and Industrial Solutions Limited': {'symbol': 'CGPOWER', 'weight': 0.0244},
    'Religare Enterprises Limited': {'symbol': 'RELIGARE', 'weight': 0.0231},
    'Bharat Dynamics Limited': {'symbol': 'BDL', 'weight': 0.0228},
    'PTC Industries Limited': {'symbol': 'PTCIL', 'weight': 0.0228},
    'Waaree Energies Limited': {'symbol': 'WAAREEENER', 'weight': 0.0214},
    'Angel One Limited': {'symbol': 'ANGELONE', 'weight': 0.0204},
    'V2 Retail Limited': {'symbol': 'V2RETAIL', 'weight': 0.0188},
    'Global Health Limited': {'symbol': 'MEDANTA', 'weight': 0.0142},
    'Titagarh Rail Systems Limited': {'symbol': 'TITAGARH', 'weight': 0.0122},
    'Swiggy Limited': {'symbol': 'SWIGGY', 'weight': 0.0066},
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
        f"Stocks Calculated - {len(portfolio)-errors}/{31} ({(calc_weight*100):.2f}% out of 97.07%)")
    print("Debt - 0%")
    print("Others (Cash, etc.) - 2.93%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 23-12-2024")

    op1 = f"{errors}"
    op2 = f"{len(portfolio)-errors}/{31} ({(calc_weight*100):.2f}% out of 97.07%) - Rest is Cash, Debt, etc."
    op3 = f"Companies, weightage, and equity-cash breakup last updated as on 23-12-2024"
    return total_change, op1, op2, op3

# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/motilal-oswal-large-and-midcap-fund-direct-plan-growth/MMO070"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    nav_element = soup.find('span', class_='amt')
    if nav_element is None:
        return -1
    prev_nav = float((nav_element.text.strip())[2:])
    return prev_nav


def run_analysis(depth, investment, units):

    file = open(
        r'C:\Users\hp\Documents\Ish\codes\self proj\project-folder-live-nav\project-folder\fund_scripts\investments.txt', 'r')
    raw_lines = file.readlines()
    if raw_lines == []:
        pass
    else:
        data = [i.split(" ") for i in [i.strip() for i in raw_lines]]
        if investment == 0:
            investment = float(data[2][0])
        if units == 0:
            units = float(data[2][1])
    file.close()

    # main:

    # fetch current nav
    previous_nav = fetch_previous_nav()
    if previous_nav == -1:
        return {
            'fund_name': "Motilal Oswal Large & Mid Cap Fund Direct Growth",
            'errors_count': "1 (Unable to fetch previous NAV of fund)",
            'stocks_calc': "Not calculated",
            'info': "Previous NAV could not be fetched",
            'prev_nav': "Not calculated",
            'estimated_nav': "Not calculated",
            'invested_amount': "Not calculated",
            'current_amount': "Not calculated",
            'profit': "Not calculated"
        }

    # calc change
    print("\nChoose depth:")
    print("1. Nominal Analysis (Fast: 15-20s)")
    print("2. In-Depth Analysis (Slow: 65-75s)")
    str = depth
    print(f"Chosen choice - {depth}")
    print()
    if str == "1":
        nav_change, op1, op2, op3 = estimate_nav_change(portfolio1)
    else:
        nav_change, op1, op2, op3 = estimate_nav_change(portfolio2)
    estimated_nav = previous_nav * (1 + nav_change)
    if op1 != "0":
        op1 += " (Could not fetch stock data of these many stocks. These are excluded from calculation)"

    # today's date
    today_date = datetime.now().strftime('%d-%m-%Y')
    yesterday_date = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')

    # print the change
    print()
    print(f'Previous NAV {yesterday_date}: ₹{previous_nav:.4f}')
    print(f'Estimated NAV {today_date}: ₹{estimated_nav:.4f}')

    # calc profit
    tot_investment = investment  # Enter Manually
    tot_units = units  # Enter Manually
    current_amt = tot_units*estimated_nav
    profit = current_amt - tot_investment

    # print profits
    print()
    print(f'Invested Amount: ₹{tot_investment:.4f}')
    print(f'Current Amount: ₹{current_amt:.4f}')

    return {
        'fund_name': "Motilal Oswal Large & Mid Cap Fund Direct Growth",
        'errors_count': f"{op1}",
        'stocks_calc': f"{op2}",
        'info': f"{op3}",
        'prev_nav': f"₹{previous_nav:.2f} ({yesterday_date})",
        'estimated_nav': f"₹{estimated_nav:.2f} ({today_date})",
        'invested_amount': f"₹{tot_investment:.2f}",
        'current_amount': f"₹{current_amt:.2f}",
        'profit': f"₹{profit:.2f}"
    }
