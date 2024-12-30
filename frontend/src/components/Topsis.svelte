<script>
  import { onMount } from "svelte";
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';
  import TopsisResults from "../components/TopsisResults.svelte";
  import Chart from "../components/Chart.svelte"; // Results component

  let weights = [];
  let criteria = [];
  let results = null;
  let dynamicResults = [];

  // Store for dynamic results
  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();
    weights = criteria.map(() => 1); // Set initial weights to 1 by default
  });

  // Function to normalize the weights so that their sum equals 1
  const normalizeWeights = () => {
    const totalWeight = weights.reduce((acc, weight) => acc + weight, 0);
    if (totalWeight !== 0) {
      // Normalize the weights to make the sum equal to 1
      weights = weights.map(weight => weight / totalWeight);
    }
    else if (totalWeight === 1) {
      // Normalize the weights to make the sum equal to 1
      weights = weights.map(weight => 1);
    }
  };

  const analyzeTOPSIS = async () => {
    // Normalize weights before sending them for analysis
    normalizeWeights();

    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/topsis', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        weights,
      }),
    });
    results = await response.json();
    // Update the dynamicResults after getting the results
    dynamicResults = results.ranked_companies.map((company, index) => ({
      name: company.name,
      score: company.score
    }));
  };
</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">TOPSIS Method</h3>

  <!-- Criteria Weights -->
  <h4 class="text-lg font-semibold text-indigo-400 mb-4 flex items-center justify-center">Weights
    <!-- Tooltip Icon -->
    <span class="ml-2 relative group">
      <span
        class="w-5 h-5 text-gray-400 hover:text-indigo-500 cursor-pointer font-bold flex items-center justify-center border border-gray-400 rounded-full"
        style="width: 1.25rem; height: 1.25rem;"
      >
        i
      </span>
      <!-- Tooltip Text -->
      <span
        class="absolute top-1/2 left-full ml-2 transform -translate-y-1/2 px-3 py-1 text-xs text-white bg-gray-700 rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10"
      >
        Weights will be normalized to sum to 1 during analysis.
      </span>
    </span>
  </h4>
  <ul class="space-y-4">
    {#each criteria as criterion, index}
      <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
        <span class="text-white">{criterion.name}</span>
        <input
          type="number"
          min="0"
          step="1"
          bind:value={weights[index]}
          class="w-24 px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        />
      </li>
    {/each}
  </ul>

  <!-- Analyze Button -->
  <button
    on:click={analyzeTOPSIS}
    class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <!-- Results Section -->
  <div class="mt-6">
    <TopsisResults {results} />
  </div>

  <!-- Chart Component -->
  <div class="mt-6">
    <Chart {dynamicResults} />
  </div>
</div>
