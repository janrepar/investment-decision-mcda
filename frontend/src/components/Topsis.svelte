<script>
  import { onMount } from "svelte";
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';

  let weights = [];
  let criteria = [];
  let results = null;

  onMount(async () => {
    const res = await fetch('/api/criteria');
    criteria = await res.json();
    weights = criteria.map(() => 1); // Default equal weights
  });

  const analyzeTOPSIS = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/topsis', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        weights,
      }),
    });
    results = await response.json();
  };
</script>

<h3>TOPSIS Method</h3>
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
<button on:click={analyzeTOPSIS}>Analyze</button>

{#if results}
  <pre>{JSON.stringify(results, null, 2)}</pre>
{/if}
