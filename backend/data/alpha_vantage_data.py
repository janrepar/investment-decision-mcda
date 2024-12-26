import requests
from app import db
from app.models import Company, FinancialIndicator

# API key for Alpha Vantage
API_KEY = 'your_api_key_here'


# Function to get data from Alpha Vantage API
def get_alpha_vantage_data(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data


# Function to update financial indicators in the database
def update_financial_indicators(company_id, roe, debt_to_equity, dividends, volatility):
    company = Company.query.get(company_id)  # Get the company object by ID

    if company:
        # Create or update the related financial indicators
        financial_indicator = FinancialIndicator.query.filter_by(company_id=company_id).first()
        if not financial_indicator:
            financial_indicator = FinancialIndicator(company_id=company_id)
            db.session.add(financial_indicator)

        financial_indicator.roe = roe
        financial_indicator.debt_to_equity_ratio = debt_to_equity
        financial_indicator.dividends = dividends
        financial_indicator.stock_volatility = volatility

        db.session.commit()


# Connect to the database and get the list of companies
def update_all_companies():
    companies = Company.query.all()  # Get all companies from the database

    for company in companies:
        symbol = company.symbol  # Use the symbol from the database

        # Get data from Alpha Vantage
        data = get_alpha_vantage_data(symbol)

        # Check if the data is available and extract relevant fields
        if 'ReturnOnEquityTTM' in data:
            roe = float(data['ReturnOnEquityTTM']) if data['ReturnOnEquityTTM'] != 'N/A' else None
        else:
            roe = None

        if 'DebtToEquity' in data:
            debt_to_equity = float(data['DebtToEquity']) if data['DebtToEquity'] != 'N/A' else None
        else:
            debt_to_equity = None

        if 'DividendYield' in data:
            dividends = float(data['DividendYield']) if data['DividendYield'] != 'N/A' else None
        else:
            dividends = None

        # Adding stock volatility (Beta)
        if 'Beta' in data:
            volatility = float(data['Beta']) if data['Beta'] != 'N/A' else None
        else:
            volatility = None

        # Update the financial indicators in the database
        update_financial_indicators(company.id, roe, debt_to_equity, dividends, volatility)

    print("Alpha Vantage data (including stock volatility) has been successfully updated in the database.")


# Run the update function directly
if __name__ == '__main__':
    update_all_companies()

