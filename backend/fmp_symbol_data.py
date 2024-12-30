import time

import requests
from app import db, create_app
from app.models import Company
from dotenv import load_dotenv
import os

load_dotenv()

# API key for Financial Modeling Prep
API_KEY = os.getenv('FMP_API_KEY')


# Function to search for symbol by company name
def search_symbol_by_name(company_name):
    try:
        url = f'https://financialmodelingprep.com/api/v3/search?query={company_name}&apikey={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad HTTP responses
        data = response.json()

        if not data or len(data) == 0:  # Handle empty response
            print(f"No symbol found for company {company_name}")
            return None

        # Filter for NASDAQ or NYSE exchange
        for company in data:
            symbol = company['symbol']
            exchange = company['exchangeShortName']

            # Check if symbol is from NASDAQ or NYSE
            if exchange in ["NASDAQ", "NYSE"]:
                return symbol  # Return the symbol if it's from NASDAQ or NYSE

            # If the symbol contains an exchange suffix (e.g., .SS, .SW), strip it
            #if '.' in symbol:
            #    symbol = symbol.split('.')[0]

            return symbol

        print(f"No NASDAQ or NYSE or SHA symbol found for company {company_name}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error searching for symbol for company {company_name}: {e}")
        return None


# Function to update symbol in the database
def update_symbol_in_db():
    companies = Company.query.all()  # Get all companies from DB

    for company in companies:
        company_name = company.name
        current_symbol = company.symbol

        # Search for the symbol by company name using the FMP API
        new_symbol = search_symbol_by_name(company_name)

        # If a new symbol is found, and it's different from the current one, update it
        if new_symbol and new_symbol != current_symbol:
            print(f"Updating symbol for {company_name} from {current_symbol} to {new_symbol}")
            company.symbol = new_symbol
            db.session.commit()
        else:
            print(f"No change in symbol for {company_name}")

        time.sleep(10)


# Run the update function directly
if __name__ == '__main__':
    # Create the Flask app and ensure the context is active
    app = create_app()

    with app.app_context():
        update_symbol_in_db()
