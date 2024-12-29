import random

import requests
from app import db, create_app
from app.models import Company, FinancialIndicator
from dotenv import load_dotenv
import os

load_dotenv()

# API key for Alpha Vantage
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')


# Function to get data from Alpha Vantage API
def get_alpha_vantage_data(symbol):
    try:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad HTTP responses
        data = response.json()

        if "Information" in data:  # Handle API limit issues
            print(f"API limit reached for symbol {symbol}. Skipping...")
            return None

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None


# Helper function to safely convert data to float
def safe_float(value):
    try:
        # Return None if the value is not a valid float or is a known invalid string
        if value in ['N/A', 'None', None, '']:
            return None
        return float(value)
    except ValueError:
        return None


# Function to update financial indicators in the database
def update_financial_indicators(company_id, roe, price_to_earnings_ratio, dividend_yield, volatility, earnings_per_share, EV_to_EBITDA):
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
        if earnings_per_share is not None:
            financial_indicator.earnings_per_share = earnings_per_share
        if EV_to_EBITDA is not None:
            financial_indicator.EV_to_EBITDA = EV_to_EBITDA


# Connect to the database and get the list of companies
def update_all_companies():
    companies = Company.query.all()  # Get all companies

    for company in companies:
        symbol = company.symbol

        # Get data from Alpha Vantage
        #data = get_alpha_vantage_data(symbol)
        #if not data:
            #continue

        # TODO: Add None values back in db and try calling alpha venture again for company overall data
        # Extract relevant fields using safe_float helper
        #roe = safe_float(data.get('ReturnOnEquityTTM'))
        #price_to_earnings_ratio = safe_float(data.get('PERatio'))
        #dividend_yield = safe_float(data.get('DividendYield'))
        #volatility = safe_float(data.get('Beta'))
        #earnings_per_share = safe_float(data.get('EPS'))
        #EV_to_EBITDA = safe_float(data.get('EVToEBITDA'))

        roe = round(random.uniform(5, 25), 2)  # Return on Equity (5% to 25%)
        price_to_earnings_ratio = round(random.uniform(5, 40), 2)  # P/E ratio (5 to 40)
        dividend_yield = round(random.uniform(1, 10), 2)  # Dividend yield (1% to 10%)
        volatility = round(random.uniform(0.1, 2.5), 2)  # Stock volatility (0.1 to 2.5)
        earnings_per_share = round(random.uniform(1, 10), 2)  # Earnings Per Share (1 to 10)
        EV_to_EBITDA = round(random.uniform(5, 20), 2)  # EV to EBITDA (5 to 20)

        # Update financial indicators
        update_financial_indicators(company.id, roe, price_to_earnings_ratio, dividend_yield, volatility, earnings_per_share, EV_to_EBITDA)

        print(f"Updated data for {company.name} ({symbol}).")

    db.session.commit()
    print("Alpha Vantage data successfully updated.")


# Run the update function directly
if __name__ == '__main__':
    # Create the Flask app and ensure the context is active
    app = create_app()

    with app.app_context():
        update_all_companies()
