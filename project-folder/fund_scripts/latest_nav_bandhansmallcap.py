import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# Add holdings in a summarised portfolio
portfolio1 = {
    'LT Foods Ltd.': {'symbol': 'LTFOODS', 'weight': 0.0262},
    'PCBL Ltd.': {'symbol': 'PCBL', 'weight': 0.0255},
    'Cholamandalam Financial Holdings Ltd.': {'symbol': 'CHOLAHLDNG', 'weight': 0.0196},
    'Sobha Ltd.': {'symbol': 'SOBHA', 'weight': 0.0179},
    'Arvind Ltd.': {'symbol': 'ARVIND', 'weight': 0.0176},
    'The South Indian Bank Ltd.': {'symbol': 'SOUTHBANK', 'weight': 0.0160},
    'Shaily Engineering Plastics Ltd.': {'symbol': 'SHAILY', 'weight': 0.0155},
    'Apar Industries Ltd.': {'symbol': 'APARINDS', 'weight': 0.0150},
}

# Add holdings in a deeper portfolio
portfolio2 = {
    'LT Foods Ltd.': {'symbol': 'LTFOODS', 'weight': 0.0262},
    'PCBL Ltd.': {'symbol': 'PCBL', 'weight': 0.0255},
    'Cholamandalam Financial Holdings Ltd.': {'symbol': 'CHOLAHLDNG', 'weight': 0.0196},
    'Sobha Ltd.': {'symbol': 'SOBHA', 'weight': 0.0179},
    'Arvind Ltd.': {'symbol': 'ARVIND', 'weight': 0.0176},
    'The South Indian Bank Ltd.': {'symbol': 'SOUTHBANK', 'weight': 0.0160},
    'Shaily Engineering Plastics Ltd.': {'symbol': 'SHAILY', 'weight': 0.0155},
    'Apar Industries Ltd.': {'symbol': 'APARINDS', 'weight': 0.0150},
    'The Karnataka Bank Ltd.': {'symbol': 'KTKBANK', 'weight': 0.0145},
    'Rashi Peripherals Ltd.': {'symbol': 'RPTECH', 'weight': 0.0142},
    'REC Ltd.': {'symbol': 'RECLTD', 'weight': 0.0128},
    'Motilal Oswal Financial Services Ltd.': {'symbol': 'MOTILALOFS', 'weight': 0.0127},
    'Nitin Spinners Ltd.': {'symbol': 'NITINSPIN', 'weight': 0.0122},
    'TVS Holdings Ltd.': {'symbol': 'TVSHLTD', 'weight': 0.0118},
    'IndusInd Bank Ltd.': {'symbol': 'INDUSINDBK', 'weight': 0.0117},
    'eClerx Services Ltd.': {'symbol': 'ECLERX', 'weight': 0.0109},
    'Shilpa Medicare Ltd.': {'symbol': 'SHILPAMED', 'weight': 0.0108},
    'Manappuram Finance Ltd.': {'symbol': 'MANAPPURAM', 'weight': 0.0108},
    'Inox Wind Energy Ltd.': {'symbol': 'INOXWIND', 'weight': 0.0106},
    'Angel One Ltd.': {'symbol': 'ANGELONE', 'weight': 0.0100},
    'GE Vernova T&D India Ltd.': {'symbol': 'GVT&D', 'weight': 0.0095},
    'Vedanta Ltd.': {'symbol': 'VEDL', 'weight': 0.0093},
    'Power Finance Corporation Ltd.': {'symbol': 'PFC', 'weight': 0.0093},
    'Kolte-Patil Developers Ltd.': {'symbol': 'KOLTEPATIL', 'weight': 0.0091},
    'Stove Kraft Ltd.': {'symbol': 'STOVEKRAFT', 'weight': 0.0091},
    'Kirloskar Ferrous Industries Ltd.': {'symbol': 'KIRLFER', 'weight': 0.0086},
    'Kirloskar Oil Engines Ltd.': {'symbol': 'KIRLOSENG', 'weight': 0.0085},
    'Godawari Power And Ispat Ltd.': {'symbol': 'GPIL', 'weight': 0.0084},
    'Inox Wind Ltd.': {'symbol': 'INOXWIND', 'weight': 0.0082},
    'PNB Housing Finance Ltd.': {'symbol': 'PNBHOUSING', 'weight': 0.0081},
    # checkbelow
    'Prestige Estates Projects Ltd.': {'symbol': 'PRESTIGE', 'weight': 0.0080},
    'Jupiter Wagons Ltd.': {'symbol': 'JWL', 'weight': 0.0079},
    'Glenmark Pharmaceuticals Ltd.': {'symbol': 'GLENMARK', 'weight': 0.0078},
    'Wockhardt Ltd.': {'symbol': 'WOCKHARDT', 'weight': 0.0076},
    'Spicejet Ltd.': {'symbol': 'SPICEJET', 'weight': 0.0074},
    'Amara Raja Energy & Mobility Ltd': {'symbol': 'AMARAJABAT', 'weight': 0.0073},
    'Aster DM Healthcare Ltd.': {'symbol': 'ASTERDM', 'weight': 0.0073},
    'Piramal Pharma Ltd.': {'symbol': 'PIRAMALENT', 'weight': 0.0073},
    'Cyient Ltd.': {'symbol': 'CYIENT', 'weight': 0.0072},
    'Varun Beverages Ltd.': {'symbol': 'VBL', 'weight': 0.0072},
    'Birlasoft Ltd.': {'symbol': 'BIRLASOFT', 'weight': 0.0071},
    'Eris Lifesciences Ltd.': {'symbol': 'ERIS', 'weight': 0.0070},
    'Fedbank Financial Services Ltd.': {'symbol': 'FEDBK', 'weight': 0.0070},
    'Updater Services Ltd.': {'symbol': 'UPDATERS', 'weight': 0.0070},
    'TARC Ltd.': {'symbol': 'TARC', 'weight': 0.0069},
    'Radico Khaitan Ltd.': {'symbol': 'RADICO', 'weight': 0.0069},
    'Repco Home Finance Ltd.': {'symbol': 'REPCOHOME', 'weight': 0.0068},
    'Quess Corp Ltd.': {'symbol': 'QUESS', 'weight': 0.0068},
    'Jubilant Pharmova Ltd.': {'symbol': 'JUBILANT', 'weight': 0.0066},
    'Punjab National Bank': {'symbol': 'PNB', 'weight': 0.0065},
    'NCC Ltd.': {'symbol': 'NCC', 'weight': 0.0065},
    'The Great Eastern Shipping Company Ltd.': {'symbol': 'GESHIP', 'weight': 0.0062},
    'Kewal Kiran Clothing Ltd.': {'symbol': 'KEWALKIRO', 'weight': 0.0062},
    'Strides Pharma Science Ltd.': {'symbol': 'STRIDES', 'weight': 0.0061},
    'SH Kelkar And Company Ltd.': {'symbol': 'SHKELKAR', 'weight': 0.0060},
    'Ethos Ltd.': {'symbol': 'ETHOS', 'weight': 0.0060},
    'Sansera Engineering Ltd.': {'symbol': 'SANSERA', 'weight': 0.0059},
    'Neuland Laboratories Ltd.': {'symbol': 'NEULANDLAB', 'weight': 0.0059},
    '360 One Wam Ltd.': {'symbol': '360ONE', 'weight': 0.0058},
    'Sunteck Realty Ltd.': {'symbol': 'SUNECKRELT', 'weight': 0.0057},
    'Hi-Tech Pipes Ltd.': {'symbol': 'HITECHPIPES', 'weight': 0.0057},
    'Computer Age Management Services Ltd.': {'symbol': 'CAMS', 'weight': 0.0057},
    'Multi Commodity Exchange Of India Ltd.': {'symbol': 'MCX', 'weight': 0.0056},
    'Bank Of Baroda': {'symbol': 'BANKBARODA', 'weight': 0.0054},
    'Signatureglobal (India) Ltd.': {'symbol': 'SIGNATURE', 'weight': 0.0052},
    'Zomato Ltd.': {'symbol': 'ZOMATO', 'weight': 0.0051},
    'Electronics Mart India Ltd.': {'symbol': 'ELECTRONICM', 'weight': 0.0051},
    'Marksans Pharma Ltd.': {'symbol': 'MARKSANS', 'weight': 0.0050},
    'NLC India Ltd.': {'symbol': 'NLCINDIA', 'weight': 0.0049},
    'Triveni Engineering & Industries Ltd.': {'symbol': 'TRIVENI', 'weight': 0.0049},
    'Baazar Style Retail Ltd.': {'symbol': 'BAZAAR', 'weight': 0.0049},
    'Aurobindo Pharma Ltd.': {'symbol': 'AUROPHARMA', 'weight': 0.0048},
    'Blue Star Ltd.': {'symbol': 'BLUESTARCO', 'weight': 0.0047},
    'Sapphire Foods India Ltd.': {'symbol': 'SAPPHIRE', 'weight': 0.0047},
    'Yatharth Hospital & Trauma Care Services Ltd.': {'symbol': 'YATHARTH', 'weight': 0.0047},
    'Power Mech Projects Ltd.': {'symbol': 'POWERMECH', 'weight': 0.0045},
    'National Aluminium Company Ltd.': {'symbol': 'NALCO', 'weight': 0.0044},
    'Godrej Industries Ltd.': {'symbol': 'GODREJIND', 'weight': 0.0044},
    'Krsnaa Diagnostics Ltd.': {'symbol': 'KRSNAA', 'weight': 0.0044},
    'Epigral Ltd.': {'symbol': 'EPIGRL', 'weight': 0.0044},
    'SBI Cards And Payment Services Ltd.': {'symbol': 'SBICARD', 'weight': 0.0043},
    'Tilaknagar Industries Ltd.': {'symbol': 'TILAKNAGAR', 'weight': 0.0042},
    'Kaynes Technology India Ltd.': {'symbol': 'KAYNESTECH', 'weight': 0.0042},
    'NA': {'symbol': 'NA', 'weight': 0.0042},
    'Reliance Industries Ltd.': {'symbol': 'RELIANCE', 'weight': 0.0041},
    'Bombay Burmah Trading Corporation Ltd.': {'symbol': 'BOMDYEING', 'weight': 0.0040},
    'KFin Technologies Ltd.': {'symbol': 'KFINTECH', 'weight': 0.0040},
    'CESC Ltd.': {'symbol': 'CESC', 'weight': 0.0038},
    'Eureka Forbes Ltd.': {'symbol': 'EUREKA', 'weight': 0.0038},
    'Sobha Ltd. - Partly Paid-up Equity Shares (Rights Issue)': {'symbol': 'SOBHA', 'weight': 0.0038},
    'UPL Ltd.': {'symbol': 'UPL', 'weight': 0.0037},
    'Krishna Institute of Medical Sciences Ltd': {'symbol': 'KIMS', 'weight': 0.0037},
    'Greenply Industries Ltd.': {'symbol': 'GREENPLY', 'weight': 0.0037},
    'Medplus Health Services Ltd.': {'symbol': 'MEDPLUS', 'weight': 0.0036},
    'Vishnu Chemicals Ltd.': {'symbol': 'VISHNU', 'weight': 0.0036},
    'Aditya Birla Sun Life AMC Ltd.': {'symbol': 'ABSLAMC', 'weight': 0.0036},
    'Arvind Smartspaces Ltd.': {'symbol': 'ARVSMART', 'weight': 0.0034},
    'Jubilant Ingrevia Ltd.': {'symbol': 'JUBILANTING', 'weight': 0.0034},
    'Astrazeneca Pharma India Ltd.': {'symbol': 'AZTPHARMA', 'weight': 0.0033},
    'Samvardhana Motherson International Ltd.': {'symbol': 'MOTHERSON', 'weight': 0.0033},
    'Lumax Auto Technologies Ltd.': {'symbol': 'LUMAXXTECH', 'weight': 0.0032},
    'Affle (India) Ltd.': {'symbol': 'AFFLE', 'weight': 0.0031},
    'Alicon Castalloy Ltd.': {'symbol': 'ALICON', 'weight': 0.0031},
    'RHI Magnesita India Ltd.': {'symbol': 'RHI', 'weight': 0.0031},
    'Cochin Shipyard Ltd.': {'symbol': 'COCHINSHIP', 'weight': 0.0031},
    'Innova Captab Ltd.': {'symbol': 'INNOVACAP', 'weight': 0.0031},
    'Bharat Dynamics Ltd.': {'symbol': 'BHARATDYN', 'weight': 0.0030},
    'Garware Hi-Tech Films Ltd.': {'symbol': 'GARWARE', 'weight': 0.0030},
    'Sterlite Technologies Ltd.': {'symbol': 'STLTECH', 'weight': 0.0030},
    'Emcure Pharmaceuticals Ltd.': {'symbol': 'EMCUR', 'weight': 0.0030},
    'EFC Ltd.': {'symbol': 'EFC', 'weight': 0.0029},
    'Inox Green Energy Services Ltd.': {'symbol': 'INOXGREEN', 'weight': 0.0029},
    'GPT Healthcare Ltd.': {'symbol': 'GPTINFRA', 'weight': 0.0029},
    'Exide Industries Ltd.': {'symbol': 'EXIDEIND', 'weight': 0.0028},
    'Orchid Pharma Ltd.': {'symbol': 'ORCHPHARMA', 'weight': 0.0028},
    'Akums Drugs And Pharmaceuticals Ltd.': {'symbol': 'AKUMS', 'weight': 0.0028},
    'Emami Ltd.': {'symbol': 'EMAMI', 'weight': 0.0026},
    'Indus Towers Ltd.': {'symbol': 'INDUSTOWER', 'weight': 0.0026},
    'Senco Gold Ltd.': {'symbol': 'SENCGOLD', 'weight': 0.0026},
    'Juniper Hotels Ltd.': {'symbol': 'JUNIPER', 'weight': 0.0026},
    'Bansal Wire Industries Ltd.': {'symbol': 'BANSAL', 'weight': 0.0026},
    'FDC Ltd.': {'symbol': 'FDC', 'weight': 0.0025},
    'JK Lakshmi Cement Ltd.': {'symbol': 'JKLAKSHMI', 'weight': 0.0025},
    'DCB Bank Ltd.': {'symbol': 'DCBBANK', 'weight': 0.0025},
    'Greenpanel Industries Ltd.': {'symbol': 'GREENPANEL', 'weight': 0.0025},
    'Archean Chemical Industries Ltd.': {'symbol': 'ARCHEANCHEM', 'weight': 0.0025},
    'Keystone Realtors Ltd': {'symbol': 'KEYSTONERLT', 'weight': 0.0025},
    'Apeejay Surrendra Park Hotels Ltd.': {'symbol': 'APEJ', 'weight': 0.0025},
    'P N Gadgil Jewellers Ltd.': {'symbol': 'PNJ', 'weight': 0.0025},
    'Crompton Greaves Consumer Electricals Ltd.': {'symbol': 'CROMPTON', 'weight': 0.0024},
    'Jyothy Labs Ltd.': {'symbol': 'JYOTHYLAB', 'weight': 0.0024},
    'Satin Creditcare Network Ltd.': {'symbol': 'SATIN', 'weight': 0.0024},
    'GMM Pfaudler Ltd.': {'symbol': 'GMMPF', 'weight': 0.0023},
    'KEC International Ltd.': {'symbol': 'KEC', 'weight': 0.0023},
    'Gulf Oil Lubricants India Ltd.': {'symbol': 'GULFOILLUB', 'weight': 0.0023},
    'JB Chemicals & Pharmaceuticals Ltd.': {'symbol': 'JBCHEM', 'weight': 0.0022},
    'Ujjivan Small Finance Bank Ltd.': {'symbol': 'UJJIVANSFB', 'weight': 0.0022},
    'Bank of India': {'symbol': 'BANKINDIA', 'weight': 0.0021},
    'Abbott India Ltd.': {'symbol': 'ABBOTTINDIA', 'weight': 0.0021},
    'Artemis Medicare Services Ltd.': {'symbol': 'ARTEMISMED', 'weight': 0.0021},
    'Orient Cement Ltd.': {'symbol': 'ORIENTCEM', 'weight': 0.0020},
    'VRL Logistics Ltd.': {'symbol': 'VRL', 'weight': 0.0020},
    'Heritage Foods Ltd.': {'symbol': 'HERITAGE', 'weight': 0.0019},
    'Rane Holdings Ltd.': {'symbol': 'RANEHOLDNG', 'weight': 0.0019},
    'Religare Enterprises Ltd.': {'symbol': 'RELIGARE', 'weight': 0.0019},
    'KRN Heat Exchanger And Refrigeration Ltd.': {'symbol': 'KRNHEX', 'weight': 0.0019},
    'Mayur Uniquoters Ltd.': {'symbol': 'MAYURUNIQ', 'weight': 0.0018},
    'Suzlon Energy Ltd.': {'symbol': 'SUZLON', 'weight': 0.0017},
    'Landmark Cars Ltd.': {'symbol': 'LANDMARK', 'weight': 0.0015},
    'DCX Systems Ltd.': {'symbol': 'DCX', 'weight': 0.0015},
    'Chemplast Sanmar Ltd.': {'symbol': 'CHEMPLAST', 'weight': 0.0014},
    'Yatra Online Ltd.': {'symbol': 'YATRAONLINE', 'weight': 0.0013},
    'IRM Energy Ltd.': {'symbol': 'IRM', 'weight': 0.0013},
    'Steel Strips Wheels Ltd.': {'symbol': 'SSWWL', 'weight': 0.0012},
    'Minda Corporation Ltd.': {'symbol': 'MINDACORP', 'weight': 0.0012},
    'Gujarat State Petronet Ltd.': {'symbol': 'GSPL', 'weight': 0.0011},
    'Godavari Biorefineries Ltd.': {'symbol': 'GODAVARI', 'weight': 0.0010},
    'Hitachi Energy India Ltd.': {'symbol': 'HITACHI', 'weight': 0.0010},
    'Indiamart Intermesh Ltd.': {'symbol': 'INDIAMART', 'weight': 0.0009},
    'E.I.D. - Parry (India) Ltd.': {'symbol': 'EIDPARRY', 'weight': 0.0009},
    'Brigade Enterprises Ltd.': {'symbol': 'BRIGADE', 'weight': 0.0004},
    'Pearl Global Industries Ltd.': {'symbol': 'PEARLIND', 'weight': 0.0003},
    'Kirloskar Brothers Ltd.': {'symbol': 'KIRLOSKAR', 'weight': 0.0002},
    'Thangamayil Jewellery Ltd.': {'symbol': 'THANGAMAYIL', 'weight': 0.0002},
    'UPL Ltd. - Right Entitlement': {'symbol': 'UPL', 'weight': 0.0002},
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
        f"Stocks Calculated - {len(portfolio)-errors}/{178} ({(calc_weight*100):.2f}% out of 90.68%)")
    print("Debt - 0%")
    print("Others (Cash, etc.) - 9.32%")
    print("\n***companies, weightage, and equity-cash breakup last updated as on 24-12-2024")

    op1 = f"{errors}"
    op2 = f"{len(portfolio)-errors}/{178} ({(calc_weight*100):.2f}% out of 93.13%) - Rest is Cash, Debt, etc."
    op3 = f"Companies, weightage, and equity-cash breakup last updated as on 23-12-2024"
    return total_change, op1, op2, op3

# fetch current nav of the fund


def fetch_previous_nav():
    search_url = "https://www.moneycontrol.com/mutual-funds/nav/bandhan-small-cap-fund-direct-plan-growth/MAG2104"
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
            investment = float(data[5][0])
        if units == 0:
            units = float(data[5][1])
    file.close()

    # main:

    # fetch current nav
    previous_nav = fetch_previous_nav()
    if previous_nav == -1:
        return {
            'fund_name': "Bandhan Small Cap Fund Direct Growth",
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
    print("2. In-Depth Analysis (Slow: 350-360s)")
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
        'fund_name': "Bandhan Small Cap Fund Direct Growth",
        'errors_count': f"{op1}",
        'stocks_calc': f"{op2}",
        'info': f"{op3}",
        'prev_nav': f"₹{previous_nav:.2f} ({yesterday_date})",
        'estimated_nav': f"₹{estimated_nav:.2f} ({today_date})",
        'invested_amount': f"₹{tot_investment:.2f}",
        'current_amount': f"₹{current_amt:.2f}",
        'profit': f"₹{profit:.2f}"
    }
