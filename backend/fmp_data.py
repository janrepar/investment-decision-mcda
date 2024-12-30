import time
from urllib.parse import quote

import requests
from app import db, create_app
from app.models import Company, FinancialIndicator
from dotenv import load_dotenv
import os

load_dotenv()

# API key for Financial Modeling Prep
API_KEY = os.getenv('FMP_API_KEY')


# Function to escape the dot in symbols for URL compatibility
def escape_symbol_for_url(symbol):
    return quote(symbol, safe='')  # Escape all characters, including dots


# Function to get data from FMP API
def get_fmp_data(symbol):
    try:
        formatted_symbol = escape_symbol_for_url(symbol)  # Format symbol for URL
        url = f'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{formatted_symbol}?apikey={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad HTTP responses
        data = response.json()

        if not data or len(data) == 0:  # Handle empty response
            print(f"No data available for symbol {symbol}")
            return None

        # Extract the first (most recent) entry
        return data[0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None


# Function to get Beta from FMP API
def get_fmp_beta(symbol):
    try:
        formatted_symbol = escape_symbol_for_url(symbol)  # Format symbol for URL
        url = f'https://financialmodelingprep.com/api/v3/profile/{formatted_symbol}?apikey={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad HTTP responses
        data = response.json()

        if not data or len(data) == 0:  # Handle empty response
            print(f"No Beta data available for symbol {symbol}")
            return None

        # Extract Beta from the first entry
        return safe_float(data[0].get('beta'))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Beta for symbol {symbol}: {e}")
        return None


# Helper function to safely convert data to float
def safe_float(value):
    try:
        if value in ['N/A', 'None', None, '']:
            return None
        return float(value)
    except ValueError:
        return None


# Function to update financial indicators in the database
def update_financial_indicators(company_id, roe, price_to_earnings_ratio, dividend_yield, volatility, eps,
                                ev_to_ebitda):
    company = Company.query.get(company_id)

    if company:
        financial_indicator = FinancialIndicator.query.filter_by(company_id=company_id).first()
        if not financial_indicator:
            financial_indicator = FinancialIndicator(company_id=company_id)
            db.session.add(financial_indicator)

        # Update only if data is available
        if roe is not None:
            financial_indicator.roe = roe
        if price_to_earnings_ratio is not None:
            financial_indicator.price_to_earnings_ratio = price_to_earnings_ratio
        if dividend_yield is not None:
            financial_indicator.dividend_yield = dividend_yield
        if volatility is not None:
            financial_indicator.stock_volatility = volatility
        if eps is not None:
            financial_indicator.earnings_per_share = eps
        if ev_to_ebitda is not None:
            financial_indicator.EV_to_EBITDA = ev_to_ebitda


# Connect to the database and update all companies
def update_all_companies():
    companies = Company.query.all()  # Get all companies

    for company in companies:
        symbol = company.symbol

        # Get data from FMP
        data = get_fmp_data(symbol)
        if not data:
            continue

        # Get Beta (Volatility)
        beta = get_fmp_beta(symbol)

        # Extract relevant fields using safe_float helper
        roe = safe_float(data.get('roeTTM'))
        price_to_earnings_ratio = safe_float(data.get('peRatioTTM'))
        dividend_yield = safe_float(data.get('dividendYieldPercentageTTM'))
        eps = safe_float(data.get('netIncomePerShareTTM'))
        ev_to_ebitda = safe_float(data.get('enterpriseValueOverEBITDATTM'))

        # Update financial indicators
        update_financial_indicators(company.id, roe, price_to_earnings_ratio, dividend_yield, beta, eps, ev_to_ebitda)

        print(f"Updated data for {company.name} ({symbol}).")
        print(roe, price_to_earnings_ratio, dividend_yield, beta, eps, ev_to_ebitda)

        time.sleep(10)

    db.session.commit()
    print("FMP data successfully updated.")


# Run the update function directly
if __name__ == '__main__':
    # Create the Flask app and ensure the context is active
    app = create_app()

    with app.app_context():
        update_all_companies()
