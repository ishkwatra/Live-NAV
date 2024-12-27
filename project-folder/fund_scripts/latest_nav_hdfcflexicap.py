import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'HDFC Bank Ltd.': {'symbol': 'HDFCBANK', 'weight': 0.0975},
    'ICICI Bank Ltd.': {'symbol': 'ICICIBANK', 'weight': 0.0971},
    'Axis Bank Ltd.': {'symbol': 'AXISBANK', 'weight': 0.0823},
    'Cipla Ltd.': {'symbol': 'CIPLA', 'weight': 0.0444},
    'Kotak Mahindra Bank Limited': {'symbol': 'KOTAKBANK', 'weight': 0.0439},
    'Maruti Suzuki India Limited': {'symbol': 'MARUTI', 'weight': 0.0418},
    'SBI Life Insurance Company Ltd.': {'symbol': 'SBILIFE', 'weight': 0.0407},
    'Bharti Airtel Ltd.': {'symbol': 'BHARTIARTL', 'weight': 0.0401},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'HDFC Bank Ltd.': {'symbol': 'HDFCBANK', 'weight': 0.0975},
    'ICICI Bank Ltd.': {'symbol': 'ICICIBANK', 'weight': 0.0971},
    'Axis Bank Ltd.': {'symbol': 'AXISBANK', 'weight': 0.0823},
    'Cipla Ltd.': {'symbol': 'CIPLA', 'weight': 0.0444},
    'Kotak Mahindra Bank Limited': {'symbol': 'KOTAKBANK', 'weight': 0.0439},
    'Maruti Suzuki India Limited': {'symbol': 'MARUTI', 'weight': 0.0418},
    'SBI Life Insurance Company Ltd.': {'symbol': 'SBILIFE', 'weight': 0.0407},
    'Bharti Airtel Ltd.': {'symbol': 'BHARTIARTL', 'weight': 0.0401},
    'HCL Technologies Ltd.': {'symbol': 'HCLTECH', 'weight': 0.0390},
    'Piramal Pharma Limited': {'symbol': 'PPLPHARMA', 'weight': 0.0294},
    'Nexus Select Trust REIT': {'symbol': 'NXST', 'weight': 0.0228},
    'State Bank of India': {'symbol': 'SBIN', 'weight': 0.0221},
    'Infosys Limited': {'symbol': 'INFY', 'weight': 0.0210},
    'Eicher Motors Ltd.': {'symbol': 'EICHERMOT', 'weight': 0.0199},
    'Apollo Hospitals Enterprise Ltd.': {'symbol': 'APOLLOHOSP', 'weight': 0.0178},
    'Bosch Limited': {'symbol': 'BOSCHLTD', 'weight': 0.0158},
    'Hyundai Motor India Limited': {'symbol': 'HYUNDAI', 'weight': 0.0147},
    'Tata Steel Ltd.': {'symbol': 'TATASTEEL', 'weight': 0.0125},
    'Power Grid Corporation of India Ltd.': {'symbol': 'POWERGRID', 'weight': 0.0124},
    'JSW Steel Ltd.': {'symbol': 'JSWSTEEL', 'weight': 0.0122},
    'Hindustan Aeronautics Limited': {'symbol': 'HAL', 'weight': 0.0122},
    'Prestige Estates Projects Ltd.': {'symbol': 'PRESTIGE', 'weight': 0.0114},
    'United Spirits Limited': {'symbol': 'UNITDSPR', 'weight': 0.0112},
    'Tech Mahindra Ltd.': {'symbol': 'TECHM', 'weight': 0.0111},
    'Sapphire Foods India Ltd.': {'symbol': 'SAPPHIRE', 'weight': 0.0096},
    'Crompton Greaves Consumer Electricals Ltd.': {'symbol': 'CROMPTON', 'weight': 0.0087},
    'DR. LAL PATHLABS Ltd.': {'symbol': 'LALPATHLAB', 'weight': 0.0084},
    # embassy office parks reit
    'The Ramco Cements Ltd.': {'symbol': 'RAMCOCEM', 'weight': 0.0077},
    'Dr. Reddys Laboratories Ltd.': {'symbol': 'DRREDDY', 'weight': 0.0074},
    'Larsen & Toubro Ltd.': {'symbol': 'LT', 'weight': 0.0074},
    'CIE AUTOMOTIVE INDIA Ltd.': {'symbol': 'CIEINDIA', 'weight': 0.0068},
    'Mahindra & Mahindra Ltd.': {'symbol': 'M&M', 'weight': 0.0067},
    'Kalpataru Power Transmission Ltd.': {'symbol': 'KPIL', 'weight': 0.0058},
    'Metropolis Healthcare Ltd.': {'symbol': 'METROPOLIS', 'weight': 0.0052},
    'Lupin Ltd.': {'symbol': 'LUPIN', 'weight': 0.0046},
    'Escorts Ltd.': {'symbol': 'ESCORTS', 'weight': 0.0043},
    # GOI1
    'Nuvoco Vistas Corporation Ltd.': {'symbol': 'NUVOCO', 'weight': 0.0037},
    'Burger King India Ltd.': {'symbol': 'RBA', 'weight': 0.0037},
    'Birlasoft Ltd.': {'symbol': 'BSOFT', 'weight': 0.0036},
    'Cyient Ltd.': {'symbol': 'CYIENT', 'weight': 0.0036},
    'ITC Limited': {'symbol': 'ITC', 'weight': 0.0035},
    'J K Lakshmi Cement Ltd.': {'symbol': 'JKLAKSHMI', 'weight': 0.0029},
    'Varroc Engineering Ltd.': {'symbol': 'VARROC', 'weight': 0.0027},
    'Zee Entertainment Enterprises Ltd.': {'symbol': 'ZEEL', 'weight': 0.0027},
    'Bank Of Baroda': {'symbol': 'BANKBARODA', 'weight': 0.0026},
    'InterGlobe Aviation Ltd.': {'symbol': 'INDIGO', 'weight': 0.0025},
    'Reliance Industries Ltd.': {'symbol': 'RELIANCE', 'weight': 0.0019},
    # GOI2
    # GOI3
    'Bharti Airtel Ltd. - Partly Paid': {'symbol': 'AIRTELPP-E1', 'weight': 0.0012},
    'Indigo Paints Ltd.': {'symbol': 'INDIGOPNTS', 'weight': 0.0012},
    'Whirlpool Of India Ltd.': {'symbol': 'WHIRLPOOL', 'weight': 0.0012},
    'Devyani International Ltd.': {'symbol': 'DEVYANI', 'weight': 0.0010},
    'Indraprastha Gas Ltd.': {'symbol': 'IGL', 'weight': 0.0010},
    'Delhivery Ltd.': {'symbol': 'DELHIVERY', 'weight': 0.0009},
    'Ramco Systems': {'symbol': 'RAMCOSYS', 'weight': 0.0009},
    # JSW Steel LTD
    # Tech mahi 2 -ve
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
        f"Stocks Calculated - {len(portfolio)-errors}/{60} ({(calc_weight*100):.2f}% out of 87.39%)")
    print("Debt - 0.76%")
    print("Others (Cash, etc.) - 11.85%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 23-12-2024")

    op1 = f"{errors}"
    op2 = f"{len(portfolio)-errors}/{60} ({(calc_weight*100):.2f}% out of 87.39%) - Rest is Cash, Debt, etc."
    op3 = f"Companies, weightage, and equity-cash breakup last updated as on 23-12-2024"
    return total_change, op1, op2, op3


# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/hdfc-flexi-cap-fund/MHD1144"
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
            investment = float(data[0][0])
        if units == 0:
            units = float(data[0][1])
    file.close()

    # main:

    # fetch current nav
    previous_nav = fetch_previous_nav()
    if previous_nav == -1:
        return {
            'fund_name': "HDFC Flexi Cap Fund Direct Growth",
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
    print("2. In-Depth Analysis (Slow: 110-120s)")
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
        'fund_name': "HDFC Flexi Cap Fund Direct Growth",
        'errors_count': f"{op1}",
        'stocks_calc': f"{op2}",
        'info': f"{op3}",
        'prev_nav': f"₹{previous_nav:.2f} ({yesterday_date})",
        'estimated_nav': f"₹{estimated_nav:.2f} ({today_date})",
        'invested_amount': f"₹{tot_investment:.2f}",
        'current_amount': f"₹{current_amt:.2f}",
        'profit': f"₹{profit:.2f}"
    }
