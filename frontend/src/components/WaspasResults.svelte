<script>
  export let results = null; // This will hold the results passed from the parent component

</script>

<div class="max-w-2xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">WASPAS Method Results</h3>

  <!-- WASPAS Results -->
  {#if results && results.WASPAS_result}
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">WASPAS Results</h4>
      <ul class="space-y-2">
        {#each results.WASPAS_result as { company_name, company_symbol, score }}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {company_name} ({company_symbol})
            </span>
            <span class="text-indigo-400 font-semibold">{score.toFixed(4)}</span>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <!-- WPM Results -->
  {#if results && results.WPM_result}
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">WPM Results</h4>
      <ul class="space-y-2">
        {#each results.WPM_result as { company_name, company_symbol, score }}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {company_name} ({company_symbol})
            </span>
            <span class="text-indigo-400 font-semibold">{score.toFixed(4)}</span>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <!-- WSM Results -->
  {#if results && results.WSM_result}
    <div class="mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-4">WSM Results</h4>
      <ul class="space-y-2">
        {#each results.WSM_result as { company_name, company_symbol, score }}
          <li class="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md border border-gray-700">
            <span class="text-white font-medium">
              {company_name} ({company_symbol})
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
