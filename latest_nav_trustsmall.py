import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'Aster DM Healthcare Limited': {'symbol': 'ASTERDM', 'weight': 0.0280},
    'Coforge Limited': {'symbol': 'COFORGE', 'weight': 0.0277},
    'Radico Khaitan Limited': {'symbol': 'RADICO', 'weight': 0.0269},
    'The Federal Bank Limited': {'symbol': 'FEDERALBNK', 'weight': 0.0267},
    'Vijaya Diagnostic Centre Limited': {'symbol': 'VIJAYA', 'weight': 0.0263},
    'The Indian Hotels Company Limited': {'symbol': 'INDHOTEL', 'weight': 0.0252},
    'Persistent Systems Limited': {'symbol': 'PERSISTENT', 'weight': 0.0251},
    'S.J.S. Enterprises Limited': {'symbol': 'SJS', 'weight': 0.0249},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'Aster DM Healthcare Limited': {'symbol': 'ASTERDM', 'weight': 0.0280},
    'Coforge Limited': {'symbol': 'COFORGE', 'weight': 0.0277},
    'Radico Khaitan Limited': {'symbol': 'RADICO', 'weight': 0.0269},
    'The Federal Bank Limited': {'symbol': 'FEDERALBNK', 'weight': 0.0267},
    'Vijaya Diagnostic Centre Limited': {'symbol': 'VIJAYA', 'weight': 0.0263},
    'The Indian Hotels Company Limited': {'symbol': 'INDHOTEL', 'weight': 0.0252},
    'Persistent Systems Limited': {'symbol': 'PERSISTENT', 'weight': 0.0251},
    'S.J.S. Enterprises Limited': {'symbol': 'SJS', 'weight': 0.0249},
    'Wockhardt Limited': {'symbol': 'WOCKPHARMA', 'weight': 0.0244},
    'Karur Vysya Bank Limited': {'symbol': 'KARURVYSYA', 'weight': 0.0243},
    'Shaily Engineering Plastics Limited': {'symbol': 'SHAILY', 'weight': 0.0239},
    'Aditya Birla Real Estate Limited': {'symbol': 'ABREL', 'weight': 0.0236},
    'KFin Technologies Limited': {'symbol': 'KFINTECH', 'weight': 0.0221},
    'The Anup Engineering Limited': {'symbol': 'ANUP', 'weight': 0.0220},
    'Central Depository Services (India) Limited': {'symbol': 'CDSL', 'weight': 0.0219},
    'Transformers And Rectifiers (India) Limited': {'symbol': 'TARIL', 'weight': 0.0218},
    'Ami Organics Limited': {'symbol': 'AMIORG', 'weight': 0.0218},
    'Triveni Turbine Limited': {'symbol': 'TRITURBINE', 'weight': 0.0218},
    'Amber Enterprises India Limited': {'symbol': 'AMBER', 'weight': 0.0211},
    'ASK Automotive Limited': {'symbol': 'ASKAUTOLTD', 'weight': 0.0202},
    'Multi Commodity Exchange of India Limited': {'symbol': 'MCX', 'weight': 0.0194},
    'Awfis Space Solutions Limited': {'symbol': 'AWFIS', 'weight': 0.0189},
    'Strides Pharma Science Limited': {'symbol': 'STAR', 'weight': 0.0188},
    'Tilaknagar Industries Limited': {'symbol': 'TI', 'weight': 0.0182},
    'Motilal Oswal Financial Services Limited': {'symbol': 'MOTILALOFS', 'weight': 0.0177},
    'Marksans Pharma Limited': {'symbol': 'MARKSANS', 'weight': 0.0173},
    'GE Vernova T&D India Limited': {'symbol': 'GVT&D', 'weight': 0.0170},
    'Welspun Corp Limited': {'symbol': 'WELCORP', 'weight': 0.0169},
    'Zen Technologies Limited': {'symbol': 'ZENTEC', 'weight': 0.0160},
    'Nuvama Wealth Management Limited': {'symbol': 'NUVAMA', 'weight': 0.0159},
    'Chalet Hotels Limited': {'symbol': 'CHALET', 'weight': 0.0158},
    'VA Tech Wabag Limited': {'symbol': 'WABAG', 'weight': 0.0158},
    'Blue Star Limited': {'symbol': 'BLUESTARCO', 'weight': 0.0155},
    'Inox Wind Limited': {'symbol': 'INOXWIND', 'weight': 0.0153},
    'PG Electroplast Limited': {'symbol': 'PGEL', 'weight': 0.0143},
    'Rainbow Childrens Medicare Limited': {'symbol': 'RAINBOW', 'weight': 0.0137},
    'Kaynes Technology India Limited': {'symbol': 'KAYNES', 'weight': 0.0135},
    'Home First Finance Company India Limited': {'symbol': 'HOMEFIRST', 'weight': 0.0135},
    'Prudent Corporate Advisory Services Limited': {'symbol': 'PRUDENT', 'weight': 0.0132},
    'Jyoti CNC Automation Limited': {'symbol': 'JYOTICNC', 'weight': 0.0129},
    'Bansal Wire Industries Limited': {'symbol': 'BANSALWIRE', 'weight': 0.0128},
    'Piramal Pharma Limited': {'symbol': 'PPLPHARMA', 'weight': 0.0114},
    'One 97 Communications Limited': {'symbol': 'PAYTM', 'weight': 0.0107},
    'Newgen Software Technologies Limited': {'symbol': 'NEWGEN', 'weight': 0.0107},
    'Artemis Medicare Services Limited': {'symbol': 'ARTEMISMED', 'weight': 0.0103},
    'Suven Pharmaceuticals Limited': {'symbol': 'SUVENPHAR', 'weight': 0.0100},
    'Avalon Technologies Limited': {'symbol': 'AVALON', 'weight': 0.0096},
    'Tega Industries Limited': {'symbol': 'TEGA', 'weight': 0.0096},
    'PCBL Limited': {'symbol': 'PCBL', 'weight': 0.0079},
    'Aditya Vision Ltd': {'symbol': 'AVL', 'weight': 0.0078},
    'Poly Medicure Limited': {'symbol': 'POLYMED', 'weight': 0.00601},
    'V2 Retail Limited': {'symbol': 'V2RETAIL', 'weight': 0.0039},
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
        f"Stocks Calculated - {len(portfolio)-errors}/{52} ({(calc_weight*100):.2f}% out of 90.98%)")
    print("Debt - 0%")
    print("Others (Cash, etc.) - 9.02%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 23-12-2024")
    return total_change

# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/trustmf-small-cap-fund-direct-plan-growth/MTRA026"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    nav_element = soup.find('span', class_='amt')
    prev_nav = float((nav_element.text.strip())[2:])
    return prev_nav

# main:


# fetch current nav
previous_nav = fetch_previous_nav()

# calc change
print("\nChoose depth:")
print("1. Nominal Analysis (Fast: 15-20s)")
print("2. In-Depth Analysis (Slow: 110-115s)")
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
tot_units = 185.533  # Enter Manually
current_amt = tot_units*estimated_nav
profit = current_amt - tot_investment

# print profits
print()
print(f'Invested Amount: ₹{tot_investment:.4f}')
print(f'Current Amount: ₹{current_amt:.4f}')
