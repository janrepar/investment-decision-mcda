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
      on:click={() => (currentMethod = "ahp")}
      class:selected={currentMethod === "ahp"}
    >
      AHP
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      on:click={() => (currentMethod = "topsis")}
      class:selected={currentMethod === "topsis"}
    >
      TOPSIS
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      on:click={() => (currentMethod = "promethee")}
      class:selected={currentMethod === "promethee"}
    >
      PROMETHEE
    </button>
    <button
      class="py-2 px-4 text-lg font-semibold text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
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
