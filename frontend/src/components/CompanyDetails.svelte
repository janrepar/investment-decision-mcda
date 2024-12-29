<script>
  import { onMount } from 'svelte';
  let companies = [];
  let selectedCompanyId = null;
  let selectedCompany = null;

  onMount(async () => {
    const res = await fetch('/api/companies');
    companies = await res.json();
  });

  async function loadDetails() {
    const res = await fetch(`/api/companies/${selectedCompanyId}`);
    selectedCompany = await res.json();
  }
</script>

<div>
  <select bind:value={selectedCompanyId} on:change={loadDetails}>
    <option value="" disabled>Select a company</option>
    {#each companies as company}
      <option value={company.id}>{company.name}</option>
    {/each}
  </select>

  {#if selectedCompany}
    <h3>{selectedCompany.name}</h3>
    <p>Symbol: {selectedCompany.symbol}</p>
    <p>Rank: {selectedCompany.rank}</p>
    <p>Years in Rank: {selectedCompany.years_in_rank}</p>
    <h4>Financial Indicators</h4>
    <ul>
      {#each selectedCompany.financial_indicators as indicator}
        <li>
          Revenue: {indicator.revenue}, Profit: {indicator.profit}
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  select {
    margin-bottom: 20px;
  }
</style>
