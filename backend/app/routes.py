from flask import jsonify, request
from flask import current_app as app
import numpy as np
from pyDecision.algorithm import ahp_method, topsis_method, promethee_ii, waspas_method

from app.models import Company, FinancialIndicator
from helpers.mcda_helpers import list_criteria, fetch_company_data, calculate_pairwise_matrix, \
    calculate_all_pairwise_matrices, aggregate_ahp_scores, list_methods


@app.route('/api/analyze/ahp', methods=['POST'])
def analyze_ahp():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs
    criteria = list_criteria()  # List of selected criteria

    # 'mean'; 'geometric' or 'max_eigen'
    weight_derivation = data.get('weight_derivation', 'geometric')  # Weight derivation method (default: 'geometric')

    # Fetch company data
    company_data = fetch_company_data(selected_companies)

    # Check if we have enough data
    if len(company_data) < 2:
        return jsonify({'error': 'At least two companies are required for analysis'}), 400

    # Validate data completeness
    for company in company_data:
        for criterion in criteria:
            if criterion['id'] not in company:
                return jsonify({'error': f'Missing data for {criterion} in one or more companies'}), 400

    # Compute pairwise comparison matrices for each criterion
    pairwise_comparison_matrices = calculate_all_pairwise_matrices(company_data, criteria)

    # Perform AHP for each criterion
    alternative_weights = []
    for criterion_name, matrix in pairwise_comparison_matrices.items():
        weights, rc = ahp_method(matrix, wd=weight_derivation)
    #    if rc > 0.1: TODO: Check how to solve high rc for profit_change_percentage
    #        return jsonify({
    #            'error': f"Inconsistent pairwise comparison for {criterion_id}. Please review the input."
    #        }), 400
        alternative_weights.append({
            "criterion": criterion_name,
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
    criterion_names = [c["name"] for c in criteria]
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
        {"name": company_data[i]["name"], "symbol": company_data[i]["symbol"], "score": relative_closeness[i], "rank": rank + 1}
        for rank, i in enumerate(np.argsort(-relative_closeness))
    ]

    return jsonify({
        'weights': weights,
        'criterion_types': criterion_types,
        'criterion_names': criterion_names,
        'ranked_companies': ranked_companies
    })


@app.route('/api/analyze/promethee', methods=['POST'])
def analyze_promethee():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs

    # Parameters for promethee
    Q = data.get("Q", [0.3] * 10)  # indifference
    S = data.get("S", [0.4] * 10)  # preference
    P = data.get("P", [0.5] * 10)  # veto
    W = data.get("W", [9.00, 8.24, 5.98, 8.48, 7.00, 6.50, 5.00, 7.80, 6.70, 5.90])  # weights
    F = data.get("F", ['t5'] * 10)  # preference functions

    criteria = list_criteria()

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

    # Vnesemo podatke za PROMETHEE
    scores = promethee_ii(decision_matrix, W=W, Q=Q, S=S, P=P, F=F, sort=True, topn=10, graph=True, verbose=True)

    scores = scores.tolist()

    # Map company names to company numbers (1 to N)
    company_names = [company["name"] for company in company_data]

    # Combine company numbers with their respective scores
    company_scores = []
    for score in scores:
        company_scores.append({
            "company_name": company_names[int(score[0]) - 1],  # Company name
            "alternative": int(score[0]),
            "score": score[1]
        })

    # Vrnemo rezultate v JSON obliki
    return jsonify({
        'scores': company_scores
    })


@app.route('/api/analyze/waspas', methods=['POST'])
def analyze_waspas():
    data = request.json
    selected_companies = data['companies']  # List of selected company IDs
    user_weights = data.get('weights')  # User-provided weights
    lambda_value = data.get("lambda_value", 0.5)  # Default lambda value (weight given to WSM and WPM method)

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

    # Validation (Ensure dataset shape, weights, and criterion_type consistency)
    if len(criterion_types) != decision_matrix.shape[1] or len(weights) != decision_matrix.shape[1]:
        return jsonify({'error': 'The number of criteria must match the dataset dimensions'}), 400

    # Call WASPAS method
    wsm, wpm, waspas = waspas_method(decision_matrix, criterion_types, weights, lambda_value, graph=True)

    # Round the results to 3 decimals
    wsm = [round(score, 3) for score in wsm]
    wpm = [round(score, 3) for score in wpm]
    waspas = [round(score, 3) for score in waspas]

    # Map company names to the results
    company_names = [company["name"] for company in company_data]  # Extract company names
    company_symbols = [company["symbol"] for company in company_data]

    # Create lists of results with company names
    wsm_results = [{"company_name": company_names[i], "company_symbol": company_symbols[i], "score": wsm[i]} for i in range(len(company_names))]
    wpm_results = [{"company_name": company_names[i], "company_symbol": company_symbols[i], "score": wpm[i]} for i in range(len(company_names))]
    waspas_results = [{"company_name": company_names[i], "company_symbol": company_symbols[i], "score": waspas[i]} for i in range(len(company_names))]

    # Sort the results based on the score in descending order
    wsm_results = sorted(wsm_results, key=lambda x: x['score'], reverse=True)
    wpm_results = sorted(wpm_results, key=lambda x: x['score'], reverse=True)
    waspas_results = sorted(waspas_results, key=lambda x: x['score'], reverse=True)

    # Return the results in JSON format
    return jsonify({
        'WSM_result': wsm_results,  # Weighted Sum Model result
        'WPM_result': wpm_results,  # Weighted Product Model result
        'WASPAS_result': waspas_results  # WASPAS combined result
    })


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


@app.route('/api/criteria', methods=['GET'])
def get_criteria():
    # Retrieve the list of all available criteria for analysis.
    criteria = list_criteria()
    return jsonify(criteria)


@app.route('/api/methods', methods=['GET'])
def get_methods():
    methods = list_methods()
    return jsonify(methods)


@app.route('/api/company/<int:company_id>', methods=['GET'])
def get_company_overview(company_id):
    # Fetch company data
    company = Company.query.get_or_404(company_id)

    # Fetch related financial indicators
    financial_data = FinancialIndicator.query.filter_by(company_id=company.id).first()

    # Structure the response
    response = {
        "company": {
            "id": company.id,
            "name": company.name,
            "symbol": company.symbol,
            "rank": company.rank,
            "rank_change": company.rank_change,
            "years_in_rank": company.years_in_rank
        },
        "financial_indicators": {
            "revenue": financial_data.revenue,
            "profit": financial_data.profit,
            "assets": financial_data.assets,
            "employees": financial_data.employees,
            "roe": financial_data.roe,
            "price_to_earnings_ratio": financial_data.price_to_earnings_ratio,
            "stock_volatility": financial_data.stock_volatility,
            "dividend_yield": financial_data.dividend_yield,
            "earnings_per_share": financial_data.earnings_per_share,
            "EV_to_EBITDA": financial_data.EV_to_EBITDA,
            "profit_change_percentage": financial_data.profit_change_percentage,
            "revenue_change_percentage": financial_data.revenue_change_percentage
        }
    }

    return jsonify(response)
