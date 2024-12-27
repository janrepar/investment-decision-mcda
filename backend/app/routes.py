from flask import jsonify, request
from flask import current_app as app
import numpy as np
from pyDecision.algorithm import ahp_method, topsis_method

from app.models import Company, FinancialIndicator
from helpers.mcda_helpers import list_criteria, fetch_company_data, calculate_pairwise_matrix, \
    calculate_all_pairwise_matrices, aggregate_ahp_scores


# TODO: Change to use all criteria (need to calculate matrices according to data in db)
@app.route('/api/analyze/ahp', methods=['POST'])
def analyze_ahp():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs
    criteria = list_criteria()  # List of selected criteria

    # 'mean'; 'geometric' or 'max_eigen'
    weight_derivation = data.get('weight_derivation', 'geometric')  # Weight derivation method (default: 'geometric')

    # Get data for the selected companies
    decision_matrices = []

    # Fetch company data
    company_data = fetch_company_data(selected_companies)

    # Check if we have enough data
    if len(company_data) < 2:
        return jsonify({'error': 'At least two companies are required for analysis'}), 400

    # Validate data completeness
    for company in company_data:
        for criterion in criteria:
            if criterion not in company:
                return jsonify({'error': f'Missing data for {criterion} in one or more companies'}), 400

    # Compute pairwise comparison matrices for each criterion
    pairwise_comparison_matrices = calculate_all_pairwise_matrices(company_data, criteria)

    # Perform AHP for each criterion
    alternative_weights = []
    for criterion_id, matrix in pairwise_comparison_matrices.items():
        weights, rc = ahp_method(matrix, weight_derivation)
        if rc > 0.1:
            return jsonify({
                'error': f"Inconsistent pairwise comparison for {criterion_id}. Please review the input."
            }), 400
        alternative_weights.append({
            "criterion": criterion_id,
            "weights": weights.tolist(),
            "consistency_ratio": rc
        })

    # Calculate criteria weights
    try:
        # Use example weights or calculate dynamically
        criteria_values = [1] * len(criteria)  # Equal weights as a placeholder
        criteria_pairwise_matrix = calculate_pairwise_matrix(criteria_values, "max")
        criteria_weights, rc = ahp_method(criteria_pairwise_matrix, weight_derivation)

        if rc > 0.1:
            return jsonify({'error': 'Inconsistent criteria comparison. Please review the criteria weights.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error calculating criteria weights: {str(e)}'}), 500

    # Calculate the final scores
    final_scores = aggregate_ahp_scores(company_data, alternative_weights, criteria_weights)

    # Return results
    return jsonify({
        'criteria_weights': criteria_weights.tolist(),
        'alternative_weights': alternative_weights,
        'aggregated_scores': final_scores
    })


@app.route('/api/analyze/topsis', methods=['POST'])
def analyze_topsis():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs
    user_weights = data.get('weights')  # Optional: User-provided weights

    # Fetch criteria metadata and determine weights/types
    criteria = list_criteria()
    criterion_types = [c["type"] for c in criteria]  # 'max' or 'min'
    default_weights = [1 / len(criteria)] * len(criteria)  # Equal weights

    # Use user-provided weights or fallback to default
    weights = user_weights if user_weights else default_weights

    # Fetch company data
    company_data = fetch_company_data(selected_companies)

    # Validate data
    if len(company_data) < 2:
        return jsonify({'error': 'At least two companies are required for analysis'}), 400

    # Build the decision matrix
    try:
        decision_matrix = np.array([
            [company[criterion["id"]] for criterion in criteria]
            for company in company_data
        ])
    except KeyError as e:
        return jsonify({'error': f'Missing data for criterion: {str(e)}'}), 400

    # Perform TOPSIS analysis
    try:
        relative_closeness = topsis_method(decision_matrix, weights, criterion_types)
    except Exception as e:
        return jsonify({'error': f'Error performing TOPSIS analysis: {str(e)}'}), 500

    # Prepare results
    ranked_companies = [
        {"name": company_data[i]["name"], "score": relative_closeness[i], "rank": rank + 1}
        for rank, i in enumerate(np.argsort(-relative_closeness))
    ]

    return jsonify({
        'weights': weights,
        'criterion_types': criterion_types,
        'ranked_companies': ranked_companies
    })


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs
    selected_criteria = data['criteria']  # List of selected criteria IDs
    weights = data['weights']  # List of criteria weights
    method = data['method']    # Selected MCDA method

    # Fetch data for selected companies and criteria
    decision_matrix = []
    for company_id in selected_companies:
        financial_data = FinancialIndicator.query.filter_by(company_id=company_id).first()
        row = []
        for criterion in selected_criteria:
            row.append(getattr(financial_data, criterion))
        decision_matrix.append(row)

    if method == 'ahp':
        decision_matrix = np.array(decision_matrix)  # Ensure it's a numpy array
        ahp = AHP(decision_matrix)
        scores = ahp.rank()  # Returns the ranked alternatives
    elif method == 'topsis':
        decision_matrix = np.array(decision_matrix)
        scores = topsis_method(decision_matrix, weights, selected_criteria)
    elif method == 'promethee':
        decision_matrix = np.array(decision_matrix)
        scores = promethee_method(decision_matrix, weights, preference_functions)
    elif method == 'wsm':
        decision_matrix = np.array(decision_matrix)
        scores = wsm_method(decision_matrix, weights)
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'results': scores})


@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    result = [
        {
            "id": company.id,
            "name": company.name,
            "symbol": company.symbol,
            "rank": company.rank,
            "rank_change": company.rank_change,
            "years_in_rank": company.years_in_rank,
        }
        for company in companies
    ]
    return jsonify(result)


@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    financial_data = [
        {
            "id": indicator.id,
            "revenue": indicator.revenue,
            "revenue_change_percentage": indicator.revenue_change_percentage,
            "profit": indicator.profit,
            "profit_change_percentage": indicator.profit_change_percentage,
            "assets": indicator.assets,
            "employees": indicator.employees,
            "roe": indicator.roe,
            "debt_to_equity_ratio": indicator.debt_to_equity_ratio,
            "stock_volatility": indicator.stock_volatility,
            "dividends": indicator.dividends
        }
        for indicator in company.financial_indicators
    ]
    return jsonify({
        "id": company.id,
        "name": company.name,
        "symbol": company.symbol,
        "rank": company.rank,
        "rank_change": company.rank_change,
        "years_in_rank": company.years_in_rank,
        "financial_indicators": financial_data
    })


@app.route('/api/criteria', methods=['GET'])
def get_criteria():
    # Retrieve the list of all available criteria for analysis.
    criteria = list_criteria()

    return jsonify(criteria)
