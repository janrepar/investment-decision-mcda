<script>
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';
  import AhpResults from "../components/AhpResults.svelte";
  import Chart from "../components/Chart.svelte";

  let weightDerivation = "geometric";
  let results = null;

  // Store for dynamic results
  let dynamicResults = [];

  const analyzeAHP = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/ahp', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        weight_derivation: weightDerivation,
      }),
    });
    results = await response.json();
    // Update the dynamicResults after getting the results
    dynamicResults = results.aggregated_scores.map((company) => ({
      name: company.name,
      score: company.score
    }));
  };
</script>

<div class="max-w-xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">AHP Method</h3>

  <!-- Weight Derivation Selection -->
  <div class="mb-4">
    <label for="weight-derivation" class="block text-white font-medium mb-2">
      Weight Derivation:
    </label>
    <select
      id="weight-derivation"
      bind:value={weightDerivation}
      class="w-full px-3 py-2 bg-gray-800 text-white border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:outline-none"
    >
      <option value="geometric" title="Uses geometric mean of pairwise comparison values.">
        Geometric
      </option>
      <option value="mean" title="Averages the pairwise comparison values.">
        Mean
      </option>
      <option value="max_eigen" title="Derives weights from the largest eigenvalue of the pairwise comparison matrix.">
        Max Eigen
      </option>
    </select>
  </div>

  <!-- Analyze Button -->
  <button
    on:click={analyzeAHP}
    class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <!-- Results Component -->
  <AhpResults {results} />

  <!-- Chart Component -->
  <div class="mt-6">
    <Chart {dynamicResults} />
  </div>
</div>
