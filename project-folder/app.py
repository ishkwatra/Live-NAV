from flask import Flask, render_template, request
# Import specific modules as needed
from fund_scripts import latest_nav_jmflexicap

app = Flask(__name__)

# Routes for the application


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/more_info')
def more_info():
    return render_template('more_info.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    fund_name = request.form['fund']  # Selected fund name
    depth = request.form['depth']    # Analysis depth (nominal or in-depth)
    investment = request.form['investment']
    units = request.form['units']
    if investment == '':
        investment = 0
    else:
        investment = int(investment)
    if units == '':
        units = 0
    else:
        units = int(units)

    # Map fund name to the corresponding module
    fund_scripts = {
        'latest_nav_hdfcflexicap': 'fund_scripts.latest_nav_hdfcflexicap',
        'latest_nav_jmflexicap': 'fund_scripts.latest_nav_jmflexicap',
        'latest_nav_motilallargeandmidcap': 'fund_scripts.latest_nav_motilallargeandmidcap',
        'latest_nav_motilalsmallcap': 'fund_scripts.latest_nav_motilalsmallcap',
        'latest_nav_trustsmallcap': 'fund_scripts.latest_nav_trustsmallcap',
        'latest_nav_bandhansmallcap': 'fund_scripts.latest_nav_bandhansmallcap'
    }

    # Dynamically import the selected script
    fund_module = __import__(fund_scripts[fund_name], fromlist=[''])
    results = fund_module.run_analysis(
        depth, investment, units)  # Execute the analysis

    # Render the results page
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
