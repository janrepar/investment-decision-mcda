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

  // Mapping preference functions to descriptive names
  const functionDescriptions = {
    t1: "Usual",
    t2: "U-Shape",
    t3: "V-Shape",
    t4: "Level",
    t5: "V-Shape with Indifference",
    t6: "Gaussian",
    t7: "C-Form"
  };

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

  const setAllFunctions = (functionType) => {
    F = F.map(() => functionType);
  };

  const normalizeWeights = () => {
    const totalWeight = W.reduce((acc, weight) => acc + weight, 0);
    if (totalWeight !== 0) {
      W = W.map(weight => weight / totalWeight);
    } else if (totalWeight === 0) {
      W = W.map(() => 1);
    }
  };

  const analyzePROMETHEE = async () => {
    // Normalize weights before sending them for analysis
    normalizeWeights();

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

    if (!response.ok) {
      // If the backend returns a consistency error
      if (results.error) {
        alert(results.error); // Display the error message as an alert
      }
      return;
    }

    // Update the dynamicResults after getting the results
    dynamicResults = results.scores.map((company) => ({
      name: company.company_name,
      score: company.score
    }));
  };
</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">PROMETHEE Method</h3>

  <!-- Set All Functions -->
  <div class="m-4">
    <label class="text-sm font-medium text-gray-400">Set All Preference Functions:</label>
    <select
      on:change={(e) => setAllFunctions(e.target.value)}
      class="ml-2 px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
    >
      <option disabled selected>Select Function</option>
      {#each Object.entries(functionDescriptions) as [value, label]}
        <option value={value}>{label}</option>
      {/each}
    </select>
  </div>

  <!-- Criteria Inputs -->
  <div class="space-y-6">
    {#each criteria as criterion, index}
      <div class="bg-gray-800 p-4 rounded-lg shadow-md">
        <h4 class="text-lg font-semibold text-indigo-400 flex items-center">

          {criterion.name}
        </h4>
        <div class="grid grid-cols-5 gap-4 mt-2">
          <!-- Q Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Indifference (Q):</label>
            <input
              type="number"
              step="0.01"
              bind:value={Q[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- S Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Gaussian (S):</label>
            <input
              type="number"
              step="0.01"
              bind:value={S[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- P Input -->
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Preference (P):</label>
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
            <label class="text-sm font-medium text-gray-400">Function:</label>
            <select
              bind:value={F[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              {#each Object.entries(functionDescriptions) as [value, label]}
                <option value={value}>{label}</option>
              {/each}
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
