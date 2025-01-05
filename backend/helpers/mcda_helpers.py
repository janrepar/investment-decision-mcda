import numpy as np

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
            # Calculate the absolute difference or ratio (ratio is relative so normalisation of values is not needed - ratio between 1000 and 1500 is the same as 1 and 1.5)
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
                intensity = map_to_intensity(ratio)

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


def preference_to_text(preferenece_num):
    mapping = {
        1: "equally preferred to",
        3: "moderately preferred to",
        5: "strongly preferred to",
        7: "very strongly preferred to",
        9: "extremely preferred to"
    }
    return mapping.get(preferenece_num, "equally preferred to")


def generate_comparison_text(matrix, companies):
    """
    Generate textual pairwise comparisons from a pairwise matrix.

    :param matrix: Pairwise comparison matrix.
    :param companies: List of company names.
    :return: List of textual comparisons.
    """
    n = len(matrix)
    comparisons = []

    for i in range(n):
        for j in range(i + 1, n):
            preference_num = matrix[i][j]
            text = preference_to_text(preference_num)
            comparisons.append(f"{companies[i]} is {text} {companies[j]}")

    return comparisons


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
        criterion_name = criterion["name"]
        criterion_type = criterion["type"]
        values = [company[criterion_id] for company in company_data]

        # Compute pairwise matrix for this criterion
        pairwise_comparisons[criterion_name] = calculate_pairwise_matrix(values, criterion_type)

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

    # Rank companies by scores
    ranked_companies = sorted(
        [{"name": company_data[i]["name"], "symbol": company_data[i]["symbol"], "score": aggregated_scores[i]} for i in range(num_companies)],
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_companies


def min_max_normalisation(decision_matrix, criterion_types):
    normalized_matrix = np.copy(decision_matrix)
    for i in range(decision_matrix.shape[1]):
        if criterion_types[i] == 'max':
            max_val = np.max(decision_matrix[:, i])
            min_val = np.min(decision_matrix[:, i])
            normalized_matrix[:, i] = (decision_matrix[:, i] - min_val) / (max_val - min_val)
        elif criterion_types[i] == 'min':
            min_val = np.min(decision_matrix[:, i])
            max_val = np.max(decision_matrix[:, i])
            normalized_matrix[:, i] = (max_val - decision_matrix[:, i]) / (max_val - min_val)
    return normalized_matrix


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
                "symbol": company.symbol,
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
        {
            "id": "revenue",
            "name": "Revenue",
            "type": "max",
            "description": "Total income generated by the company before expenses."
        },
        {
            "id": "profit",
            "name": "Profit",
            "type": "max",
            "description": "Net income after deducting all expenses from revenue."
        },
        {
            "id": "profit_change_percentage",
            "name": "Profit Change (%)",
            "type": "max",
            "description": "Percentage change in profit compared to the previous period."
        },
        {
            "id": "revenue_change_percentage",
            "name": "Revenue Change (%)",
            "type": "max",
            "description": "Percentage change in revenue compared to the previous period."
        },
        {
            "id": "roe",
            "name": "Return on Equity (ROE)",
            "type": "max",
            "description": "A measure of profitability relative to shareholders' equity."
        },
        {
            "id": "price_to_earnings_ratio",
            "name": "Price To Earnings Ratio",
            "type": "min",
            "description": "Valuation metric comparing the company's share price to its earnings per share."
        },
        {
            "id": "stock_volatility",
            "name": "Stock Volatility",
            "type": "min",
            "description": "A measure of how much the company's stock price fluctuates over time."
        },
        {
            "id": "dividend_yield",
            "name": "Dividend Yield",
            "type": "max",
            "description": "Annual dividend payments as a percentage of the stock's price."
        },
        {
            "id": "earnings_per_share",
            "name": "Earnings Per Share",
            "type": "max",
            "description": "Portion of the company's profit allocated to each outstanding share."
        },
        {
            "id": "EV_to_EBITDA",
            "name": "EV To EBITDA",
            "type": "min",
            "description": "Enterprise value compared to earnings before interest, taxes, depreciation, and amortization. Used for valuation."
        }
    ]


def list_methods():
    return [
        {
            "id": "ahp",
            "name": "AHP (Analytic Hierarchy Process)",
            "description": (
                "AHP is a structured decision-making framework that uses pairwise comparisons to determine "
                "the relative importance of criteria and alternatives. It helps in ranking based on a hierarchy "
                "of criteria and sub-criteria."
            )
        },
        {
            "id": "topsis",
            "name": "TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)",
            "description": (
                "TOPSIS is a multi-criteria decision analysis method that identifies the best option "
                "by comparing each to an ideal solution. It considers the distance to the ideal and "
                "negative-ideal solutions for ranking."
            )
        },
        {
            "id": "promethee",
            "name": "PROMETHEE (Preference Ranking Organization Method for Enrichment Evaluations)",
            "description": (
                "PROMETHEE is a decision-making method that ranks alternatives based on pairwise comparisons "
                "using preference functions. It is especially useful for handling both quantitative and qualitative "
                "criteria in complex decision problems."
            )
        },
        {
            "id": "waspas",
            "name": "WASPAS (Weighted Aggregated Sum Product Assessment)",
            "description": (
                "WASPAS combines the Weighted Sum Model (WSM) and Weighted Product Model (WPM) methods "
                "to rank options based on criteria. It provides an efficient way to handle multi-criteria "
                "decision-making problems."
            )
        },
        {
            "id": "wsm",
            "name": "WSM (Weighted Sum Model)",
            "description": (
                "WSM evaluates options by calculating the weighted sum of the criteria for each. "
                "It assumes all criteria are additive and independent."
            )
        },
        {
            "id": "wpm",
            "name": "WPM (Weighted Product Model)",
            "description": (
                "WPM evaluates options by multiplying the criteria values raised to their respective weights. "
                "It is suitable when criteria are multiplicative."
            )
        }
    ]


