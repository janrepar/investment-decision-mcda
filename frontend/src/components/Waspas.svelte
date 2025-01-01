<script>
  import { onMount } from "svelte";
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';
  import WaspasResults from "../components/WaspasResults.svelte";
  import Chart from "../components/Chart.svelte";
  import WaspasChart from "../components/WaspasChart.svelte"; // Results component

  let weights = [];
  let lambda = 0.5;
  let criteria = [];
  let results = null;

  // Store for dynamic results
  let dynamicResults = [];

  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();
    weights = criteria.map(() => 1); // Default weight of 1 for each criterion
  });

  const analyzeWASPAS = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/waspas', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        weights,
        lambda_value: lambda,
      }),
    });
    results = await response.json();

    if (!response.ok) {
      // If the backend returns a consistency error
      if (results.error) {
        alert(results.error); // Display the error message as an alert
      }
      return;
    }

    // Update the dynamicResults after getting the results
    // Set results for all methods
    dynamicResults = results.WASPAS_result.map((company) => ({
      name: company.company_name,
      waspasScore: company.score,
      wpmScore: results.WPM_result.find(result => result.company_name === company.company_name)?.score || 0,
      wsmScore: results.WSM_result.find(result => result.company_name === company.company_name)?.score || 0
    }));
  };
</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">WASPAS Method</h3>

  <!-- Lambda Input -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-300 mb-2">
      Lambda Value (0 to 1):
    </label>
    <input
      type="number"
      min="0"
      max="1"
      step="0.1"
      bind:value={lambda}
      class="w-full px-3 py-2 bg-gray-800 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
    />
  </div>

  <!-- Criteria Weights -->
  <h4 class="text-lg font-semibold text-indigo-400 mb-4">Weights</h4>
  <ul class="space-y-4">
    {#each criteria as criterion, index}
      <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
        <span class="text-white">{criterion.name}</span>
        <input
          type="number"
          min="0"
          bind:value={weights[index]}
          class="w-24 px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        />
      </li>
    {/each}
  </ul>

  <!-- Analyze Button -->
  <button
    on:click={analyzeWASPAS}
    class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <!-- Results Section -->
  <div class="mt-6">
    <WaspasResults {results} />
  </div>

   <!-- Chart Component -->
  <div class="mt-6">
    <WaspasChart {dynamicResults} />
  </div>

</div>
