import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'VA Tech Wabag Ltd.': {'symbol': 'WABAG', 'weight': 0.0422},
    'Vijaya Diagnostic Centre Ltd.': {'symbol': 'VIJAYA', 'weight': 0.0354},
    'Shaily Engineering Plastics Ltd.': {'symbol': 'SHAILY', 'weight': 0.0343},
    'INEOS Styrolution India Ltd.': {'symbol': 'STYRENIX', 'weight': 0.0326},
    'V-Guard Industries Ltd.': {'symbol': 'VGUARD', 'weight': 0.0325},
    'CCL Products (India) Ltd.': {'symbol': 'CCL', 'weight': 0.0324},
    'Karur Vysya Bank Ltd.': {'symbol': 'KARURVYSYA', 'weight': 0.0315},
    'Triveni Turbine Ltd.': {'symbol': 'TRITURBINE', 'weight': 0.0291},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'VA Tech Wabag Ltd.': {'symbol': 'WABAG', 'weight': 0.0422},
    'Vijaya Diagnostic Centre Ltd.': {'symbol': 'VIJAYA', 'weight': 0.0354},
    'Shaily Engineering Plastics Ltd.': {'symbol': 'SHAILY', 'weight': 0.0343},
    'INEOS Styrolution India Ltd.': {'symbol': 'STYRENIX', 'weight': 0.0326},
    'V-Guard Industries Ltd.': {'symbol': 'VGUARD', 'weight': 0.0325},
    'CCL Products (India) Ltd.': {'symbol': 'CCL', 'weight': 0.0324},
    'Karur Vysya Bank Ltd.': {'symbol': 'KARURVYSYA', 'weight': 0.0315},
    'Triveni Turbine Ltd.': {'symbol': 'TRITURBINE', 'weight': 0.0291},
    'Pricol Ltd.': {'symbol': 'PRICOLLTD', 'weight': 0.0282},
    'V-Mart Retail Ltd.': {'symbol': 'VMART', 'weight': 0.0279},
    'Rainbow Children\'s Medicare Ltd.': {'symbol': 'RAINBOW', 'weight': 0.0275},
    'Sky Gold Ltd.': {'symbol': 'SKYGOLD', 'weight': 0.0260},
    'KEC International Ltd.': {'symbol': 'KEC', 'weight': 0.0257},
    'Apar Industries Ltd.': {'symbol': 'APARINDS', 'weight': 0.0247},
    'Pitti Engineering Ltd.': {'symbol': 'PITTIENG', 'weight': 0.0242},
    'eClerx Services Ltd.': {'symbol': 'ECLERX', 'weight': 0.0232},
    'Rossari Biotech Ltd.': {'symbol': 'ROSSARI', 'weight': 0.0229},
    'Zomato Ltd.': {'symbol': 'ZOMATO', 'weight': 0.0226},
    'Campus Activewear Ltd.': {'symbol': 'CAMPUS', 'weight': 0.0216},
    'Multi Commodity Exchange Of India Ltd.': {'symbol': 'MCX', 'weight': 0.0215},
    'Praj Industries Ltd.': {'symbol': 'PRAJIND', 'weight': 0.0213},
    'V2 Retail Ltd.': {'symbol': 'V2RETAIL', 'weight': 0.0206},
    'Blue Star Ltd.': {'symbol': 'BLUESTARCO', 'weight': 0.0190},
    'Godrej Agrovet Ltd.': {'symbol': 'GODREJAGRO', 'weight': 0.0185},
    'Transformers And Rectifiers India Ltd.': {'symbol': 'TARIL', 'weight': 0.0185},
    'GE Vernova T&D India Ltd.': {'symbol': 'GVT&D', 'weight': 0.0183},
    'Voltas Ltd.': {'symbol': 'VOLTAS', 'weight': 0.0182},
    'Inox Wind Ltd.': {'symbol': 'INOXWIND', 'weight': 0.0179},
    'Chalet Hotels Ltd.': {'symbol': 'CHALET', 'weight': 0.0179},
    'Bharat Electronics Ltd.': {'symbol': 'BEL', 'weight': 0.0178},
    'Premier Energies Limited': {'symbol': 'PREMIERENE', 'weight': 0.0172},
    'Mphasis Ltd.': {'symbol': 'MPHASIS', 'weight': 0.0167},
    'Cholamandalam Financial Holdings Ltd.': {'symbol': 'CHOLAHLDNG', 'weight': 0.0155},
    'Trent Ltd.': {'symbol': 'TRENT', 'weight': 0.0153},
    'Zen Technologies Ltd.': {'symbol': 'ZENTEC', 'weight': 0.0150},
    'Cyient DLM Ltd.': {'symbol': 'CYIENTDLM', 'weight': 0.0148},
    'Varroc Engineering Ltd.': {'symbol': 'VARROC', 'weight': 0.0147},
    'Gufic Biosciences Ltd.': {'symbol': 'GUFICBIO', 'weight': 0.0136},
    'Sagility India Ltd.': {'symbol': 'SAGILITY', 'weight': 0.0131},
    'Electrosteel Castings Ltd.': {'symbol': 'ELECTCAST', 'weight': 0.0131},
    'P N Gadgil Jewellers Ltd.': {'symbol': 'PNGJL', 'weight': 0.0127},
    'Five-Star Business Finance Ltd.': {'symbol': 'FIVESTAR', 'weight': 0.0124},
    'Hyundai Motor India Ltd.': {'symbol': 'HYUNDAI', 'weight': 0.0032},
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

    op1 = f"{errors}"
    op2 = f"{len(portfolio)-errors}/{43} ({(calc_weight*100):.2f}% out of 93.13%) - Rest is Cash, Debt, etc."
    op3 = f"Companies, weightage, and equity-cash breakup last updated as on 24-12-2024"
    return total_change, op1, op2, op3

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


def run_analysis(depth, investment, units):

    file = open(
        r'C:\Users\hp\Documents\Ish\codes\self proj\project-folder-live-nav\project-folder\fund_scripts\investments.txt', 'r')
    raw_lines = file.readlines()
    if raw_lines == []:
        pass
    else:
        data = [i.split(" ") for i in [i.strip() for i in raw_lines]]
        if investment == 0:
            investment = float(data[3][0])
        if units == 0:
            units = float(data[3][1])
    file.close()

    # main:

    # fetch current nav
    previous_nav = fetch_previous_nav()
    if previous_nav == -1:
        return {
            'fund_name': "Motilal Oswal Small Cap Fund Direct Growth",
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
    print("2. In-Depth Analysis (Slow: 90-100s)")
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
        'fund_name': "Motilal Oswal Small Cap Fund Direct Growth",
        'errors_count': f"{op1}",
        'stocks_calc': f"{op2}",
        'info': f"{op3}",
        'prev_nav': f"₹{previous_nav:.2f} ({yesterday_date})",
        'estimated_nav': f"₹{estimated_nav:.2f} ({today_date})",
        'invested_amount': f"₹{tot_investment:.2f}",
        'current_amount': f"₹{current_amt:.2f}",
        'profit': f"₹{profit:.2f}"
    }
