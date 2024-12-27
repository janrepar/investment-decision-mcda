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

    # Define thresholds for intensity mapping
    thresholds = {
        1: 0.05,  # Equal importance for differences below 5%
        3: 0.2,   # Moderate importance for differences between 5% and 20%
        5: 0.5,   # Strong importance for differences between 20% and 50%
        7: 0.8,   # Very strong importance for differences between 50% and 80%
        9: 1.0    # Extreme importance for differences above 80%
    }

    for i in range(n):
        for j in range(i + 1, n):
            # Calculate the absolute difference or ratio
            if data[j] == 0 or data[i] == 0:
                intensity = 1  # Avoid division by zero; treat as equal importance
            else:
                # Calculate relative ratio or difference
                if criterion_type == "max":  # Benefit criterion
                    ratio = abs(data[i] - data[j]) / max(data[i], data[j])
                elif criterion_type == "min":  # Cost criterion
                    ratio = abs(data[j] - data[i]) / max(data[i], data[j])  # Reverse logic for cost

                # Assign intensity based on thresholds
                if ratio <= thresholds[1]:
                    intensity = 1
                elif ratio <= thresholds[3]:
                    intensity = 3
                elif ratio <= thresholds[5]:
                    intensity = 5
                elif ratio <= thresholds[7]:
                    intensity = 7
                else:
                    intensity = 9

            # Populate the pairwise comparison matrix
            if criterion_type == "max":  # Benefit criterion
                if data[i] > data[j]:
                    matrix[i][j] = intensity
                    matrix[j][i] = 1 / intensity
                elif data[i] < data[j]:
                    matrix[i][j] = 1 / intensity
                    matrix[j][i] = intensity
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1  # Equal importance for identical values
            elif criterion_type == "min":  # Cost criterion
                if data[i] < data[j]:  # Reverse logic for costs
                    matrix[i][j] = intensity
                    matrix[j][i] = 1 / intensity
                elif data[i] > data[j]:
                    matrix[i][j] = 1 / intensity
                    matrix[j][i] = intensity
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1  # Equal importance for identical values

    return matrix


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
                "debt_to_equity_ratio": financial_data.debt_to_equity_ratio,
                "stock_volatility": financial_data.stock_volatility,
                "dividends": financial_data.dividends
            })
    return company_data


def list_criteria():
    return [
        {"id": "revenue", "name": "Revenue", "type": "max"},
        {"id": "profit", "name": "Profit", "type": "max"},
        {"id": "profit_change_percentage", "name": "Profit Change (%)", "type": "max"},
        {"id": "revenue_change_percentage", "name": "Revenue Change (%)", "type": "max"},
        {"id": "roe", "name": "Return on Equity (ROE)", "type": "max"},
        {"id": "debt_to_equity_ratio", "name": "Debt to Equity Ratio", "type": "min"},
        {"id": "stock_volatility", "name": "Stock Volatility", "type": "min"},
        {"id": "dividends", "name": "Dividends", "type": "max"}
    ]




def topsis_method(decision_matrix, weights, criteria_types):
    # Create a decision matrix and weights
    decision_matrix = np.array(decision_matrix)
    weights = np.array(weights)

    # Perform TOPSIS analysis
    topsis = topsis_method(decision_matrix, weights, criteria_types)
    scores = topsis.rank()  # Returns the ranked alternatives
    return scores


def promethee_method(decision_matrix, weights, preference_functions):
    # Create decision matrix and weights
    decision_matrix = np.array(decision_matrix)
    weights = np.array(weights)

    # Define preference functions, and perform PROMETHEE analysis
    promethee = promethee_method(decision_matrix, weights, preference_functions)
    positive_flows, negative_flows, net_flows = promethee.flow()  # Returns preference flows
    return net_flows


def wsm_method(decision_matrix, weights):
    # Create decision matrix and weights
    decision_matrix = np.array(decision_matrix)
    weights = np.array(weights)

    # Perform WSM analysis
    wsm = wsm_method(decision_matrix, weights)
    scores = wsm.rank()  # Returns the ranked alternatives
    return scores