from app import db
from app.models import Company, FinancialIndicator
import json


# Helper function to convert formatted numbers
def convert_to_number(value):
    if not value or value == "N/A":
        return 0.0
    return float(value.replace("$", "").replace(",", ""))


# Helper function to convert percentage to floats
def convert_percentage_to_float(value):
    if not value or value == "N/A":
        return 0.0
    return float(value.replace("%", "").strip()) / 100


# Insert data into the database
def insert_company_data():
    # Load JSON data from file
    with open('companies.json', 'r') as file:
        fortune_500_data = json.load(file)

    for company_data in fortune_500_data:
        company = Company(
            name=company_data['name'],
            symbol=company_data['symbol'],
            rank=int(company_data['rank']),
            rank_change=company_data['rank_change'],
            years_in_rank=int(company_data['years_in_rank'])
        )
        db.session.add(company)
        db.session.commit()  # Commit to generate company.id

        financial_indicator = FinancialIndicator(
            company_id=company.id,
            revenue=convert_to_number(company_data['revenue']),
            profit=convert_to_number(company_data['profit']),
            profit_change=company_data['profit_change'],
            revenue_change=company_data['revenue_change'],
            assets=convert_to_number(company_data['assets']),
            employees=int(company_data['employees'].replace(",", "")),
            profit_change_percentage=convert_percentage_to_float(company_data['profit_change']),
            revenue_change_percentage=convert_percentage_to_float(company_data['revenue_change'])
        )
        db.session.add(financial_indicator)

    db.session.commit()

    print("Data has been successfully inserted into the database.")


# Run the update function directly
if __name__ == '__main__':
    insert_company_data()
