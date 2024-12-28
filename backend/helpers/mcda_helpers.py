import numpy as np
from pyDecision.algorithm import ahp_method

from app.models import Company, FinancialIndicator


def calculate_pairwise_matrix(data, criterion_type):
    """
    Calculate pairwise comparison for input data.

    :param data: Data array for one criterion for each company (e.g. revenues)
    :param criterion_type: Type of criterion (max for benefit, min for cost)
    :return: Comparison matrix for specific criterion and companies.
    """
    # Example revenues for three companies: data = [320430.5, 400000, 350000]
    n = len(data)
    matrix = np.ones((n, n))  # Initialize with 1s for diagonal values

    for i in range(n):
        for j in range(i + 1, n):
            # Calculate the absolute difference or ratio
            if data[i] == 0 or data[j] == 0:
                intensity = 1  # Avoid division by zero; treat as equal
            else:
                # Calculate ratio or reverse ratio based on criterion type
                if criterion_type == "max":  # Benefit criterion
                    ratio = abs(abs(data[i]) - abs(data[j])) / max(abs(data[i]), abs(data[j]))
                elif criterion_type == "min":  # Cost criterion
                    ratio = abs(abs(data[j]) - abs(data[i])) / max(abs(data[i]), abs(data[j]))  # Reverse logic for cost
                else:
                    raise ValueError("Invalid criterion_type. Use 'max' or 'min'.")

                # Determine intensity based on the ratio
                intensity = map_to_intensity_smooth(ratio)

            # Populate the pairwise comparison matrix
            if criterion_type == "max":  # Benefit criterion
                if abs(data[i]) > abs(data[j]):
                    matrix[i][j] = intensity
                    matrix[j][i] = 1 / intensity
                elif abs(data[i]) < abs(data[j]):
                    matrix[i][j] = 1 / intensity
                    matrix[j][i] = intensity
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1  # Equal importance for identical values
            elif criterion_type == "min":  # Cost criterion
                if abs(data[i]) < abs(data[j]):  # Reverse logic for costs
                    matrix[i][j] = intensity
                    matrix[j][i] = 1 / intensity
                elif abs(data[i]) > abs(data[j]):
                    matrix[i][j] = 1 / intensity
                    matrix[j][i] = intensity
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1  # Equal importance for identical values

    return matrix


def map_to_intensity_smooth(ratio):
    return min(9, max(1, round(9 / (1 + np.exp(-10 * (ratio - 0.5))))))


def map_to_intensity(ratio):
    if ratio <= 0.10:
        return 1
    elif ratio <= 0.25:
        return 3
    elif ratio <= 0.45:
        return 5
    elif ratio <= 0.75:
        return 7
    else:
        return 9


def calculate_all_pairwise_matrices(company_data, criteria):
    """
    Calculate pairwise comparison matrices for all criteria.

    :param company_data: Company data.
    :param criteria: List of criteria metadata from list_criteria().
    :return: Dictionary of pairwise matrices for each criterion.
    """
    pairwise_comparisons = {}

    for criterion in criteria:
        criterion_id = criterion["id"]
        criterion_type = criterion["type"]
        values = [company[criterion_id] for company in company_data]

        # Compute pairwise matrix for this criterion
        pairwise_comparisons[criterion_id] = calculate_pairwise_matrix(values, criterion_type)

    return pairwise_comparisons


def aggregate_ahp_scores(company_data, alternative_weights, criteria_weights):
    """
    Aggregate the AHP scores for ranking companies.

    :param alternative_weights: List of weights for each criterion (alternative weights).
    :param company_data: List of company data with financial indicators.
    :param criteria_weights: List of weights for each criterion.
    :return: Aggregated scores for each company.
    """
    num_companies = len(company_data)
    aggregated_scores = [0] * num_companies  # Initialize scores for all companies

    # Calculate aggregated scores
    for criterion_index, criterion_weights in enumerate(alternative_weights):
        criterion_weight = criteria_weights[criterion_index]
        for i, weight in enumerate(criterion_weights["weights"]):
            aggregated_scores[i] += weight * criterion_weight

    # Normalize scores (optional for scaling between 0 and 1)
    total_score = sum(aggregated_scores)
    if total_score > 0:  # Avoid division by zero
        normalized_scores = [score / total_score for score in aggregated_scores]
    else:
        normalized_scores = aggregated_scores  # Use raw scores if total is 0

    # Rank companies by scores
    ranked_companies = sorted(
        [{"name": company_data[i]["name"], "score": normalized_scores[i]} for i in range(num_companies)],
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_companies


def fetch_company_data(selected_company_ids):
    """
    Fetch company data and financial indicators for selected companies.

    :param selected_company_ids: List of company IDs to fetch data for.
    :return: Dictionary containing company names and financial indicators.
    """
    companies = Company.query.filter(Company.id.in_(selected_company_ids)).all()
    company_data = []

    for company in companies:
        # Fetch related financial indicators
        financial_data = FinancialIndicator.query.filter_by(company_id=company.id).first()
        if financial_data:
            company_data.append({
                "name": company.name,
                "revenue": financial_data.revenue,
                "profit": financial_data.profit,
                "profit_change_percentage": financial_data.profit_change_percentage,
                "revenue_change_percentage": financial_data.revenue_change_percentage,
                "roe": financial_data.roe,
                "price_to_earnings_ratio": financial_data.price_to_earnings_ratio,
                "stock_volatility": financial_data.stock_volatility,
                "dividend_yield": financial_data.dividend_yield,
                "earnings_per_share": financial_data.earnings_per_share,
                "EV_to_EBITDA": financial_data.EV_to_EBITDA
            })
    return company_data


def list_criteria():
    return [
        {"id": "revenue", "name": "Revenue", "type": "max"},
        {"id": "profit", "name": "Profit", "type": "max"},
        {"id": "profit_change_percentage", "name": "Profit Change (%)", "type": "max"},
        {"id": "revenue_change_percentage", "name": "Revenue Change (%)", "type": "max"},
        {"id": "roe", "name": "Return on Equity (ROE)", "type": "max"},
        {"id": "price_to_earnings_ratio", "name": "Price To Earnings Ratio", "type": "min"},
        {"id": "stock_volatility", "name": "Stock Volatility", "type": "min"},
        {"id": "dividend_yield", "name": "Dividend Yield", "type": "max"},
        {"id": "earnings_per_share", "name": "Earnings Per Share", "type": "max"},
        {"id": "EV_to_EBITDA", "name": "EV To EBITDA", "type": "min"}
    ]
