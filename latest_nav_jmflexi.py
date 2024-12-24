import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'HDFC Bank Ltd.': {'symbol': 'HDFCBANK', 'weight': 0.0727},
    'ICICI Bank Ltd.': {'symbol': 'ICICIBANK', 'weight': 0.0498},
    'Infosys Ltd.': {'symbol': 'INFY', 'weight': 0.0438},
    'State Bank of India': {'symbol': 'SBIN', 'weight': 0.0423},
    'Bharti Airtel Ltd.': {'symbol': 'BHARTIARTL', 'weight': 0.0342},
    'Tech Mahindra Ltd.': {'symbol': 'TECHM', 'weight': 0.0274},
    'Larsen & Toubro Ltd.': {'symbol': 'LT', 'weight': 0.0272},
    "Dr. Reddy's Laboratories Ltd.": {'symbol': 'DRREDDY', 'weight': 0.0245},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'HDFC Bank Ltd.': {'symbol': 'HDFCBANK', 'weight': 0.0727},
    'ICICI Bank Ltd.': {'symbol': 'ICICIBANK', 'weight': 0.0498},
    'Infosys Ltd.': {'symbol': 'INFY', 'weight': 0.0438},
    'State Bank of India': {'symbol': 'SBIN', 'weight': 0.0423},
    'Bharti Airtel Ltd.': {'symbol': 'BHARTIARTL', 'weight': 0.0342},
    'Tech Mahindra Ltd.': {'symbol': 'TECHM', 'weight': 0.0274},
    'Larsen & Toubro Ltd.': {'symbol': 'LT', 'weight': 0.0272},
    "Dr. Reddy's Laboratories Ltd.": {'symbol': 'DRREDDY', 'weight': 0.0245},
    'Biocon Ltd.': {'symbol': 'BIOCON', 'weight': 0.0240},
    'Samvardhana Motherson International': {'symbol': 'MOTHERSON', 'weight': 0.0236},
    'ITC Ltd.': {'symbol': 'ITC', 'weight': 0.0234},
    'REC Ltd.': {'symbol': 'RECLTD', 'weight': 0.0213},
    'KEC International Ltd.': {'symbol': 'KEC', 'weight': 0.0212},
    'CESC Ltd.': {'symbol': 'CESC', 'weight': 0.0197},
    'ICRA Ltd.': {'symbol': 'ICRA', 'weight': 0.0181},
    'Deepak Fertilisers And Petrochemicals': {'symbol': 'DEEPAKFERT', 'weight': 0.0179},
    'Amber Enterprises India Ltd.': {'symbol': 'AMBER', 'weight': 0.0162},
    'Mrs. Bectors Food Specialities Ltd.': {'symbol': 'BECTORFOOD', 'weight': 0.0162},
    'Arvind Ltd.': {'symbol': 'ARVIND', 'weight': 0.0159},
    'Bajaj Auto Ltd.': {'symbol': 'BAJAJ-AUTO', 'weight': 0.0159},
    'Exide Industries Ltd.': {'symbol': 'EXIDEIND', 'weight': 0.0152},
    'Petronet LNG Ltd.': {'symbol': 'PETRONET', 'weight': 0.0148},
    'Sun Pharmaceutical Industries Ltd.': {'symbol': 'SUNPHARMA', 'weight': 0.0145},
    'Siemens Ltd.': {'symbol': 'SIEMENS', 'weight': 0.0145},
    'PG Electroplast Ltd.': {'symbol': 'PGEL', 'weight': 0.0137},
    'Ambuja Cements Ltd.': {'symbol': 'AMBUJACEM', 'weight': 0.0136},
    'Glenmark Pharmaceuticals Ltd.': {'symbol': 'GLENMARK', 'weight': 0.0134},
    'Multi Commodity Exchange Of India Ltd.': {'symbol': 'MCX', 'weight': 0.0133},
    'Indigo Paints Ltd.': {'symbol': 'INDIGOPNTS', 'weight': 0.0133},
    'Hindalco Industries Ltd.': {'symbol': 'HINDALCO', 'weight': 0.0131},
    'Blue Star Ltd.': {'symbol': 'BLUESTARCO', 'weight': 0.0128},
    'Zomato Ltd.': {'symbol': 'ZOMATO', 'weight': 0.0127},
    'Suven Pharmaceuticals Ltd.': {'symbol': 'SUVENPHAR', 'weight': 0.0124},
    'Gujarat State Petronet Ltd.': {'symbol': 'GSPL', 'weight': 0.0121},
    'Neuland Laboratories Ltd.': {'symbol': 'NEULANDLAB', 'weight': 0.0118},
    'Strides Pharma Science Ltd.': {'symbol': 'STAR', 'weight': 0.0117},
    'Newgen Software Technologies Ltd.': {'symbol': 'NEWGEN', 'weight': 0.0117},
    'Devyani International Ltd.': {'symbol': 'DEVYANI', 'weight': 0.0116},
    'Equitas Small Finance Bank Ltd.': {'symbol': 'EQUITASBNK', 'weight': 0.0115},
    'JSW Infrastructure Ltd.': {'symbol': 'JSWINFRA', 'weight': 0.0111},
    'Tata Technologies Ltd.': {'symbol': 'TATATECH', 'weight': 0.0105},
    'Kirloskar Oil Engines Ltd.': {'symbol': 'KIRLOSENG', 'weight': 0.0104},
    'HEG Ltd.': {'symbol': 'HEG', 'weight': 0.0102},
    'India Glycols Ltd.': {'symbol': 'INDIAGLYCO', 'weight': 0.0099},
    'Orchid Pharma Ltd.': {'symbol': 'ORCHPHARMA', 'weight': 0.0099},
    'Gulf Oil Lubricants India Ltd.': {'symbol': 'GULFOILLUB', 'weight': 0.0097},
    'Bharat Electronics Ltd.': {'symbol': 'BEL', 'weight': 0.0092},
    'Jyothy Labs Ltd.': {'symbol': 'JYOTHYLAB', 'weight': 0.0090},
    'BASF India Ltd.': {'symbol': 'BASF', 'weight': 0.0087},
    'Global Health Ltd.': {'symbol': 'MEDANTA', 'weight': 0.0086},
    'Power Grid Corporation Of India Ltd.': {'symbol': 'POWERGRID', 'weight': 0.0085},
    'Restaurant Brands Asia Ltd.': {'symbol': 'RBA', 'weight': 0.0085},
    'ICICI Prudential Life Insurance Company Ltd.': {'symbol': 'ICICIPRULI', 'weight': 0.0083},
    'Thomas Cook (India) Ltd.': {'symbol': 'THOMASCOOK', 'weight': 0.0081},
    'SAMHI Hotels Ltd.': {'symbol': 'SAMHI', 'weight': 0.0075},
    'Dhanuka Agritech Ltd.': {'symbol': 'DHANUKA', 'weight': 0.0068},
    'Signatureglobal (India) Ltd.': {'symbol': 'SIGNATURE', 'weight': 0.0061},
    'Schaeffler India Ltd.': {'symbol': 'SCHAEFFLER', 'weight': 0.0056},
    'Ahluwalia Contracts (India) Ltd.': {'symbol': 'AHLUCONT', 'weight': 0.0048},
    'Motilal Oswal Financial Services Ltd.': {'symbol': 'MOTILALOFS', 'weight': 0.0040},
    'Amara Raja Energy & Mobility Ltd.': {'symbol': 'ARE&M', 'weight': 0.0036},
    'Asian Paints Ltd.': {'symbol': 'ASIANPAINT', 'weight': 0.0034},
    'Pidilite Industries Ltd.': {'symbol': 'PIDILITIND', 'weight': 0.0034},
    'Polyplex Corporation Ltd.': {'symbol': 'POLYPLEX', 'weight': 0.0005},
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
        f"Stocks Calculated - {len(portfolio)-errors}/{64} ({(calc_weight*100):.2f}% out of 98.93%)")
    print("Debt - 0%")
    print("Others (Cash, etc.) - 1.07%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 23-12-2024")
    return total_change

# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/jm-flexi-cap-fund-direct-growth/MJM320"
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
print("2. In-Depth Analysis (Slow: 130-135s)")
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
tot_units = 16.865  # Enter Manually
current_amt = tot_units*estimated_nav
profit = current_amt - tot_investment

# print profits
print()
print(f'Invested Amount: ₹{tot_investment:.4f}')
print(f'Current Amount: ₹{current_amt:.4f}')
