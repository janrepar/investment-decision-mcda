<script>
  import { writable } from "svelte/store";

  export let results = null; // Data for Promethee results
  const showDetails = writable(false);

  const toggleDetails = () => {
    showDetails.update((state) => !state);
  };
</script>

<div class="max-w-3xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">Promethee Results</h3>

  {#if results}
    <!-- Ranked Companies -->
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">Company Rankings</h4>
      <ul class="space-y-2">
        {#each results.scores as { company_name, score }, index}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {index + 1}. {company_name}
            </span>
            <span class="text-indigo-400 font-semibold">{score.toFixed(4)}</span>
          </li>
        {/each}
      </ul>
    </div>
  {:else}
    <!-- Handle Null Results -->
    <p class="text-gray-400 text-center">No results available. Please run the analysis to see the results.</p>
  {/if}
</div>
