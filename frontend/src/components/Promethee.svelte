<script>
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';
  import { onMount } from "svelte";
  import PrometheeResults from "../components/PrometheeResults.svelte";
  import Chart from "../components/Chart.svelte";

  let Q = [];
  let S = [];
  let P = [];
  let W = [];
  let F = [];
  let criteria = [];
  let results = null;

  // Store for dynamic results
  let dynamicResults = [];

  // Fetch criteria on mount
  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();

    // Initialize arrays based on criteria length
    Q = criteria.map(() => 0.3); // Example default
    S = criteria.map(() => 0.4);
    P = criteria.map(() => 0.5);
    W = criteria.map(() => 1);
    F = criteria.map(() => "t5");
  });

  const analyzePROMETHEE = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/promethee', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        Q,
        S,
        P,
        W,
        F,
      }),
    });
    results = await response.json();
    // Update the dynamicResults after getting the results
    dynamicResults = results.scores.map((company) => ({
      name: company.company_name,
      score: company.score
    }));
  };
</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">PROMETHEE Method</h3>

  <!-- Criteria Inputs -->
  <div class="space-y-6">
    {#each criteria as criterion, index}
      <div class="bg-gray-800 p-4 rounded-lg shadow-md">
        <h4 class="text-lg font-semibold text-indigo-400">{criterion.name}</h4>
        <div class="grid grid-cols-5 gap-4 mt-2">
          <!-- Q Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Q:</label>
            <input
              type="number"
              step="0.01"
              bind:value={Q[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- S Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">S:</label>
            <input
              type="number"
              step="0.01"
              bind:value={S[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- P Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">P:</label>
            <input
              type="number"
              step="0.01"
              bind:value={P[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- W Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Weight (W):</label>
            <input
              type="number"
              min="0"
              bind:value={W[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- F Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Function (F):</label>
            <select
              bind:value={F[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              <option value="t1">Type 1</option>
              <option value="t2">Type 2</option>
              <option value="t3">Type 3</option>
              <option value="t4">Type 4</option>
              <option value="t5">Type 5</option>
            </select>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Analyze Button -->
  <button
    on:click={analyzePROMETHEE}
    class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <!-- Results Component -->
  <PrometheeResults {results} />

  <!-- Chart Component -->
  <div class="mt-6">
    <Chart {dynamicResults} />
  </div>
</div>
