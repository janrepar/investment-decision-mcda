<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  export let results = null;
  const showDetails = writable(false);

  const toggleDetails = () => {
    showDetails.update((state) => !state);
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
        <!-- Weights for Each Criterion -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Weights by Criterion</h4>
          {#each results.alternative_weights as { criterion, weights, consistency_ratio }}
            <div class="mb-4 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
              <h5 class="text-white font-medium mb-2">
                {criterion} (Consistency Ratio: {consistency_ratio.toFixed(4)})
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

        <!-- Criteria Weights -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Criteria Weights</h4>
          <ul class="space-y-1 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            {#each results.criteria_weights as weight, index}
              <li class="flex justify-between text-sm text-gray-300">
                <span>{results.alternative_weights[index]?.criterion || `Criterion ${index + 1}`}</span>
                <span>{weight.toFixed(4)}</span>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {/if}
  {:else}
    <!-- Handle Null Results -->
    <p class="text-gray-400 text-center">No results available. Please run the analysis to see the results.</p>
  {/if}
</div>
