<script>
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';

  // let Q = [0.3, 0.3, 0.3];
  // let S = [0.4, 0.4, 0.4];
  // let P = [0.5, 0.5, 0.5];
  // let W = [1, 1, 1];
  // let F = ["t5", "t5", "t5"];
  let results = null;

  const analyzePROMETHEE = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/promethee', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({companies: companyIds}),
    });
    results = await response.json();
  };
</script>

<h3>PROMETHEE Method</h3>
<!-- Inputs for Q, S, P, W, F -->
<button on:click={analyzePROMETHEE}>Analyze</button>

{#if results}
  <pre>{JSON.stringify(results, null, 2)}</pre>
{/if}
