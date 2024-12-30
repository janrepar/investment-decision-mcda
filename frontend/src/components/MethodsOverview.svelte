<script>
  import { onMount } from 'svelte';

  let methods = [];
  let criteria = [];

  onMount(async () => {
    // Fetch methods
    const methodsRes = await fetch('/api/methods');
    methods = await methodsRes.json();

    // Fetch criteria
    const criteriaRes = await fetch('/api/criteria');
    criteria = await criteriaRes.json();
  });
</script>

<div class="max-w-3xl mt-16 mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">Methods and Criteria Overview</h3>

  <!-- Methods Section -->
  <div class="bg-gray-800 p-4 rounded-lg mb-6">
    <h4 class="text-lg font-semibold text-indigo-400 mb-2">Methods</h4>
    <ul class="space-y-4 text-left">
      {#each methods as method}
        <li class="text-white">
          <strong>{method.name}:</strong> {method.description}
        </li>
      {/each}
    </ul>
  </div>

  <!-- Criteria Section -->
  <div class="bg-gray-800 p-4 rounded-lg">
    <h4 class="text-lg font-semibold text-indigo-400 mb-2">Criteria</h4>
    <ul class="space-y-4 text-left">
      {#each criteria as criterion}
        <li class="text-white">
          <strong>{criterion.name}:</strong> {criterion.description}
          (<i>{criterion.type === 'max' ? 'Maximization' : 'Minimization'}</i>)
        </li>
      {/each}
    </ul>
  </div>
</div>
