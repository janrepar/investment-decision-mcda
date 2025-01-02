<script>
  import { writable } from "svelte/store";

  export let results = null;
  const showDetails = writable(false);
  const showTable = writable(false); // State for showing the popup table

  const toggleDetails = () => {
    showDetails.update((state) => !state);
  };

  const toggleTable = () => {
    showTable.update((state) => !state);
  };
</script>

<div class="max-w-3xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">AHP Results</h3>

  {#if results}
    <!-- Aggregated Scores and Rankings -->
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">Company Rankings</h4>
      <ul class="space-y-2">
        {#each results.aggregated_scores as { name, symbol, score }, index}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {index + 1}. {name} ({symbol})
            </span>
            <span class="text-indigo-400 font-semibold">{score.toFixed(4)}</span>
          </li>
        {/each}
      </ul>
    </div>

    <!-- Show Table Button -->
    <button
      on:click={toggleTable}
      class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
    >
      Show Criteria Table
    </button>

    <!-- Show More Button -->
    <button
      on:click={toggleDetails}
      class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
    >
      {#if $showDetails} Hide Details {/if}
      {#if !$showDetails} More Details {/if}
    </button>

    <!-- Additional Details -->
    {#if $showDetails}
      <div class="mt-6 space-y-6">
        <!-- Company Priority Vectors -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Company Priority Vectors</h4>
          {#each results.alternative_weights as { criterion, weights, consistency_ratio }}
            <div class="mb-4 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
              <h5 class="text-white font-medium mb-2">
                {criterion}
              </h5>
              <ul class="space-y-1">
                {#each weights as weight, index}
                  <li class="flex justify-between text-sm text-gray-300">
                    <span>{results.aggregated_scores[index].name} ({results.aggregated_scores[index].symbol})</span>
                    <span>{weight.toFixed(4)}</span>
                  </li>
                {/each}
              </ul>
            </div>
          {/each}
        </div>

        <!-- Criteria Priority Vectors -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Criteria Priority Vectors</h4>
          <ul class="space-y-1 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            {#each results.criteria_weights as weight, index}
              <li class="flex justify-between text-sm text-gray-300">
                <span>{results.alternative_weights[index]?.criterion || `Criterion ${index + 1}`}</span>
                <span>{weight.toFixed(4)}</span>
              </li>
            {/each}
          </ul>
        </div>

        <!-- Comparisons Section -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Pairwise Comparisons</h4>
          {#each Object.entries(results.comparisons) as [criterion, comparisonList]}
            <div class="mb-4 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
              <h5 class="text-white font-medium mb-2">{criterion}</h5>
              <ul class="space-y-1">
                {#each comparisonList as comparison}
                  <li class="text-sm text-gray-300">{comparison}</li>
                {/each}
              </ul>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  {:else}
    <!-- Handle Null Results -->
    <p class="text-gray-400 text-center">No results available. Please run the analysis to see the results.</p>
  {/if}
</div>

<!-- Popup Table -->
{#if $showTable}
  <div class="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-95 z-50">
    <div class="bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600 w-full max-h-[95vh] max-w-[85vw] overflow-auto">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">Company Priority Vectors</h4>
      <table class="min-w-full bg-gray-800 rounded-lg shadow-md border border-gray-700">
        <thead>
          <tr>
            <th class="text-center py-2 px-4 text-gray-300">Company</th>
            {#each results.criteria_weights as criterion, index}
              <th class="text-left py-2 px-4 text-gray-300">{results.alternative_weights[index]?.criterion || `Criterion ${index + 1}`}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each results.aggregated_scores as { name, symbol, score }, index}
            <tr class="border-b border-gray-700">
              <td class="py-2 px-4 text-white">{name} ({symbol})</td>
              {#each results.criteria_weights as weight, critIndex}
                <td class="py-2 px-4 text-gray-300">{results.alternative_weights[critIndex]?.weights[index]?.toFixed(4) || 'N/A'}</td>
              {/each}
            </tr>
          {/each}

          <!-- Last row for the priority vectors -->
          <tr class="border-t border-gray-700">
            <td class="py-2 px-4 text-white font-semibold">Criteria Priority Vectors</td>
            {#each results.criteria_weights as weight}
              <td class="py-2 px-4 text-gray-300">{weight.toFixed(4)}</td>
            {/each}
          </tr>
        </tbody>
      </table>
      <button
        on:click={toggleTable}
        class="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
      >
        Close Table
      </button>
    </div>
  </div>
{/if}
