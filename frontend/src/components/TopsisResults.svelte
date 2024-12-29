<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  export let results = null;
  export let criteria_names = []; // Array of criteria names
  const showDetails = writable(false);

  const toggleDetails = () => {
    showDetails.update((state) => !state);
  };
</script>

<div class="max-w-3xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">TOPSIS Results</h3>

  {#if results}
    <!-- Ranked Companies -->
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">Company Rankings</h4>
      <ul class="space-y-2">
        {#each results.ranked_companies as { name, rank, score }}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {rank}. {name}
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
        <!-- Criteria Types and Weights -->
        <div>
          <h4 class="text-lg font-semibold text-indigo-400 mb-4">Criteria Weights</h4>
          <ul class="space-y-1 bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            {#each results.criterion_types as type, index}
              <li class="flex justify-between text-sm text-gray-300">
                <span class="text-white">
                  {results.criterion_names[index]} ({type === "max" ? "Benefit" : "Cost"})
                </span>
                <span>{results.weights[index].toFixed(4)}</span>
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
