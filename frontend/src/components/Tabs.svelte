<script>
  import AHP from '././Ahp.svelte';
  import TOPSIS from '././Topsis.svelte';
  import PROMETHEE from '././Promethee.svelte';
  import WASPAS from '././Waspas.svelte';

  let currentMethod = "ahp";
</script>

<div class="space-y-4">
  <p class="text-lg text-gray-400 mt-8">Choose a method:</p>
  <!-- Tab Buttons -->
  <div class="flex justify-center space-x-8">
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      title="Analytic Hierarchy Process (AHP) is a structured decision-making framework that uses pairwise comparisons to determine the relative importance of criteria and alternatives. It helps in ranking based on a hierarchy of criteria and sub-criteria."
      on:click={() => (currentMethod = "ahp")}
      class:selected={currentMethod === "ahp"}
    >
      AHP
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      title="Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision analysis method that identifies the best option by comparing each to an ideal solution. It considers the distance to the ideal and negative-ideal solutions for ranking."
      on:click={() => (currentMethod = "topsis")}
      class:selected={currentMethod === "topsis"}
    >
      TOPSIS
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      title="Preference Ranking Organization Method for Enrichment Evaluations (PROMETHEE) is a decision-making method that ranks alternatives based on pairwise comparisons using preference functions. It is especially useful for handling both quantitative and qualitative criteria in complex decision problems."
      on:click={() => (currentMethod = "promethee")}
      class:selected={currentMethod === "promethee"}
    >
      PROMETHEE
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      title="Weighted Aggregated Sum Product Assessment (WASPAS) combines the Weighted Sum Model (WSM) and Weighted Product Model (WPM) methods to rank options based on criteria. It provides an efficient way to handle multi-criteria decision-making problems."
      on:click={() => (currentMethod = "waspas")}
      class:selected={currentMethod === "waspas"}
    >
      WASPAS
    </button>
  </div>

  <!-- Tab Content -->
  <div class="mt-6">
    {#if currentMethod === "ahp"}
      <AHP />
    {/if}
    {#if currentMethod === "topsis"}
      <TOPSIS />
    {/if}
    {#if currentMethod === "promethee"}
      <PROMETHEE />
    {/if}
    {#if currentMethod === "waspas"}
      <WASPAS />
    {/if}
  </div>
</div>
