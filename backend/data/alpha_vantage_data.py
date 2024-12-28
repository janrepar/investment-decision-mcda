import requests
from app import db
from app.models import Company, FinancialIndicator
from dotenv import load_dotenv
import os
import time

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

        if "Note" in data:  # Handle API limit issues
            print(f"API limit reached for symbol {symbol}. Skipping...")
            return None

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None


# Function to update financial indicators in the database
def update_financial_indicators(company_id, roe, debt_to_equity, dividends, volatility):
    company = Company.query.get(company_id)

    if company:
        financial_indicator = FinancialIndicator.query.filter_by(company_id=company_id).first()
        if not financial_indicator:
            financial_indicator = FinancialIndicator(company_id=company_id)
            db.session.add(financial_indicator)

        # Update only if data is available
        if roe is not None:
            financial_indicator.roe = roe
        if debt_to_equity is not None:
            financial_indicator.debt_to_equity_ratio = debt_to_equity
        if dividends is not None:
            financial_indicator.dividends = dividends
        if volatility is not None:
            financial_indicator.stock_volatility = volatility


# Connect to the database and get the list of companies
def update_all_companies():
    companies = Company.query.all()  # Get all companies

    for company in companies:
        symbol = company.symbol

        # Get data from Alpha Vantage
        data = get_alpha_vantage_data(symbol)
        if not data:
            continue

        # Extract relevant fields
        roe = float(data['ReturnOnEquityTTM']) if data.get('ReturnOnEquityTTM') and data['ReturnOnEquityTTM'] != 'N/A' else None
        debt_to_equity = float(data['DebtToEquity']) if data.get('DebtToEquity') and data['DebtToEquity'] != 'N/A' else None
        dividends = float(data['DividendYield']) if data.get('DividendYield') and data['DividendYield'] != 'N/A' else None
        volatility = float(data['Beta']) if data.get('Beta') and data['Beta'] != 'N/A' else None

        # Update financial indicators
        update_financial_indicators(company.id, roe, debt_to_equity, dividends, volatility)

        print(f"Updated data for {company.name} ({symbol}).")

        # Avoid hitting the API rate limit
        time.sleep(1)

    db.session.commit()
    print("Alpha Vantage data successfully updated.")


# Run the update function directly
if __name__ == '__main__':
    update_all_companies()
