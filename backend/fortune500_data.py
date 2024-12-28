from app import db, create_app
from app.models import Company, FinancialIndicator
import json


# Helper function to convert formatted numbers
def convert_to_number(value):
    if not value or value == "N/A":
        return 0.0
    return float(value.replace("$", "").replace(",", ""))


# Helper function to convert percentage to floats
def convert_percentage_to_float(value):
    if not value or value == "N/A" or value == "-":
        return 0.0
    return float(value.replace("%", "").strip()) / 100


# Insert data into the database
def insert_company_data():
    # Load JSON data from file
    with open('data/companies.json', 'r') as file:
        fortune_500_data = json.load(file)

    # List to hold all the company and financial indicator objects
    companies = []
    financial_indicators = []

    for company_data in fortune_500_data:
        company = Company(
            name=company_data['name'],
            symbol=company_data['symbol'],
            rank=int(company_data['rank']),
            rank_change=company_data['rank_change'],
            years_in_rank=int(company_data['years_in_rank'])
        )
        companies.append(company)

        # Creating financial indicator for the company
        financial_indicator = FinancialIndicator(
            company=company,  # Use the company instance created earlier
            revenue=convert_to_number(company_data['revenue']),
            profit=convert_to_number(company_data['profit']),
            profit_change=company_data['profit_change'],
            revenue_change=company_data['revenue_change'],
            assets=convert_to_number(company_data['assets']),
            employees=int(company_data['employees'].replace(",", "")),
            profit_change_percentage=convert_percentage_to_float(company_data['profit_change']),
            revenue_change_percentage=convert_percentage_to_float(company_data['revenue_change'])
        )
        financial_indicators.append(financial_indicator)

    # Add all companies and financial indicators to the session at once
    db.session.bulk_save_objects(companies)
    db.session.bulk_save_objects(financial_indicators)

    # Commit all changes at once
    db.session.commit()

    print("Data has been successfully inserted into the database.")


# Run the update function directly
if __name__ == '__main__':
    # Create the Flask app and ensure the context is active
    app = create_app()

    with app.app_context():
        insert_company_data()
