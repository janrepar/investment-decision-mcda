<script>
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';

  let weightDerivation = "geometric";
  let criteriaWeights = [];
  let results = null;

  const analyzeAHP = async () => {
    let companyIds = [];
    selectedCompanies.subscribe(companies => {
      companyIds = companies.map(company => company.id);
    });

    const response = await fetch('/api/analyze/ahp', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: companyIds,
        weight_derivation: weightDerivation,
      }),
    });
    results = await response.json();
  };
</script>

<h3>AHP Method</h3>
<label>
  Weight Derivation:
  <select bind:value={weightDerivation}>
    <option value="geometric">Geometric</option>
    <option value="mean">Mean</option>
    <option value="max_eigen">Max Eigen</option>
  </select>
</label>
<button on:click={analyzeAHP}>Analyze</button>

{#if results}
  <pre>{JSON.stringify(results, null, 2)}</pre>
{/if}
