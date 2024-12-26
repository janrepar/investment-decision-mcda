from . import db


# Table for companies
class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    rank = db.Column(db.Integer)
    rank_change = db.Column(db.String)
    years_in_rank = db.Column(db.Integer)

    # Relationship to financial indicators
    financial_indicators = db.relationship('FinancialIndicator', backref='company', lazy=True)


# Table for financial indicators
class FinancialIndicator(db.Model):
    __tablename__ = 'financial_indicators'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    revenue = db.Column(db.Integer)
    profit = db.Column(db.Integer)
    profit_change = db.Column(db.String)
    revenue_change = db.Column(db.String)
    assets = db.Column(db.Integer)
    employees = db.Column(db.Integer)
    roe = db.Column(db.Float)  # Return on Equity
    debt_to_equity_ratio = db.Column(db.Float)
    stock_volatility = db.Column(db.Float)
    dividends = db.Column(db.Float)
    profit_change_percentage = db.Column(db.Float)  # Profit change as percentage
    revenue_change_percentage = db.Column(db.Float)  # Revenue change as percentage
