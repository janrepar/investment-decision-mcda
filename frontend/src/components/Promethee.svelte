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

  let dynamicResults = [];

  const functionDescriptions = {
    t1: "Usual: Best for qualitative criteria with a few distinct levels.",
    t2: "U-Shape: Includes an indifference threshold; use for criteria with small tolerances.",
    t3: "V-Shape: Suitable for quantitative criteria with no indifference threshold.",
    t4: "Level: For qualitative criteria with multiple levels and modulated preference.",
    t5: "Linear: Best for quantitative criteria with an indifference threshold.",
    t6: "Gaussian: Smooth preference progression for quantitative criteria; uses an S threshold.",
    t7: "C-Form: For advanced preference modeling (rarely used)."
  };

  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();

    Q = criteria.map(() => 0.3);
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
    } else {
      W = W.map(() => 1);
    }
  };

  const analyzePROMETHEE = async () => {
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
      if (results.error) {
        alert(results.error);
      }
      return;
    }

    dynamicResults = results.scores.map((company) => ({
      name: company.company_name,
      score: company.score
    }));
  };
</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">PROMETHEE Method</h3>

  <div class="m-4 relative">
  <label class="text-sm font-medium text-gray-400">Set All Preference Functions:</label>
  <select
    on:change={(e) => setAllFunctions(e.target.value)}
    class="ml-2 px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none relative"
  >
    <option disabled selected>Select Function</option>
    {#each Object.entries(functionDescriptions) as [value, description]}
      <option value={value} title={description}>{description.split(":")[0]}</option>
    {/each}
  </select>
</div>


  <div class="space-y-6">
    {#each criteria as criterion, index}
      <div class="bg-gray-800 p-4 rounded-lg shadow-md">
        <h4 class="text-lg font-semibold text-indigo-400 flex items-center">{criterion.name}</h4>
        <div class="grid grid-cols-5 gap-4 mt-2">
          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Indifference (Q):</label>
            <input
              type="number"
              step="0.01"
              bind:value={Q[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Gaussian (S):</label>
            <input
              type="number"
              step="0.01"
              bind:value={S[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Preference (P):</label>
            <input
              type="number"
              step="0.01"
              bind:value={P[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div class="flex flex-col">
            <label class="text-sm font-medium text-gray-400">Weight (W):</label>
            <input
              type="number"
              min="0"
              bind:value={W[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div class="flex flex-col relative">
            <label class="text-sm font-medium text-gray-400">Function:</label>
            <select
              bind:value={F[index]}
              class="px-2 py-1 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              {#each Object.entries(functionDescriptions) as [value, description]}
                <option value={value} title={description}>{description.split(":")[0]}</option>
              {/each}
            </select>
            <div
              class="absolute top-full mt-1 px-3 py-2 bg-gray-700 text-gray-200 text-xs rounded shadow"
              style="display: none;"
            >
              {functionDescriptions[F[index]]}
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <button
    on:click={analyzePROMETHEE}
    class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <PrometheeResults {results} />

  <div class="mt-6">
    <Chart {dynamicResults} />
  </div>
</div>
