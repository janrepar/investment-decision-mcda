from app import db, create_app
from app.models import Company, FinancialIndicator
import json


# Helper function to convert formatted numbers
def convert_to_number(value):
    if not value or value == "N/A":
        return 0.0
    return float(value.replace("$", "").replace(",", ""))


# Helper function to convert percentage to floats (rounded to 2 decimals)
def convert_percentage_to_float(value):
    if not value or value == "N/A" or value == "-":
        return 0.0
    return round(float(value.replace("%", "").strip()) / 100, 2)


# Insert data into the database
def insert_company_data():
    # Load JSON data from file
    with open('data/companies.json', 'r') as file:
        fortune_500_data = json.load(file)

    for company_data in fortune_500_data:
        # Check if the company already exists (by name or symbol)
        company = Company.query.filter_by(name=company_data['name']).first()
        # Create the company object
        if not company:
            # If the company doesn't exist, create and insert it
            company = Company(
                name=company_data['name'],
                symbol=company_data['symbol'],
                rank=int(company_data['rank']),
                rank_change=company_data['rank_change'],
                years_in_rank=int(company_data['years_in_rank'])
            )
            db.session.add(company)
            db.session.commit()  # Commit to ensure company.id is generated

            # Now create the financial indicator for the company
            financial_indicator = FinancialIndicator(
                company_id=company.id,  # Link the financial indicator to the company
                revenue=convert_to_number(company_data['revenue']),
                profit=convert_to_number(company_data['profit']),
                profit_change=company_data['profit_change'],
                revenue_change=company_data['revenue_change'],
                assets=convert_to_number(company_data['assets']),
                employees=int(company_data['employees'].replace(",", "")),
                profit_change_percentage=convert_percentage_to_float(company_data['profit_change']),
                revenue_change_percentage=convert_percentage_to_float(company_data['revenue_change'])
            )
            # Add financial indicator to the session
            db.session.add(financial_indicator)
            db.session.commit()

    # Commit all financial indicators at once after all companies are processed


    print("Data has been successfully inserted into the database.")


# Run the update function directly
if __name__ == '__main__':
    # Create the Flask app and ensure the context is active
    app = create_app()

    with app.app_context():
        insert_company_data()
