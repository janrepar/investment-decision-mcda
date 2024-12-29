<script>
  import { onMount } from "svelte";
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';

  let weights = [];
  let lambda = 0.5;
  let criteria = [];
  let results = null;

  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();
    weights = criteria.map(() => 1);
  });

  const analyzeWASPAS = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/waspas', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ companies: companyIds, weights, lambda_value: lambda }),
    });
    results = await response.json();
  };
</script>

<h3>WASPAS Method</h3>
<label>
  Lambda Value:
  <input type="number" min="0" max="1" step="0.1" bind:value={lambda} />
</label>
<ul>
  {#each criteria as criterion, index}
    <li>
      {criterion.name}
      <input
        type="number"
        min="0"
        value={weights[index]}
        on:input={(e) => (weights[index] = parseFloat(e.target.value))}
      />
    </li>
  {/each}
</ul>
<button on:click={analyzeWASPAS}>Analyze</button>

{#if results}
  <pre>{JSON.stringify(results, null, 2)}</pre>
{/if}
