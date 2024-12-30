<script>
  import { onMount } from 'svelte';

  let companies = []; // List of companies to populate the dropdown
  let selectedCompanyId = null; // ID of the selected company
  let company = {}; // Company details
  let financialIndicators = {}; // Financial indicators

  // Fetch the list of companies on component mount
  onMount(async () => {
    const res = await fetch('/api/companies');
    const data = await res.json();
    companies = data;
  });

  // Fetch the selected company details and financial indicators
  const fetchCompanyData = async () => {
    if (selectedCompanyId) {
      const res = await fetch(`/api/company/${selectedCompanyId}`);
      const data = await res.json();
      company = data.company;
      financialIndicators = data.financial_indicators;
    }
  };
</script>

<div class="max-w-3xl mt-16 mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">Company Overview</h3>

  <!-- Dropdown for selecting company -->
  <div class="mb-6">
    <label class="text-white font-semibold mr-4">Select Company:</label>
    <select
      bind:value={selectedCompanyId}
      on:change={fetchCompanyData}
      class="px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
    >
      <option value="" disabled>Select a company</option>
      {#each companies as company}
        <option value={company.id}>
          {company.name} ({company.symbol})
        </option>
      {/each}
    </select>
  </div>

  <!-- Company Info -->
  {#if company.name}
    <div class="bg-gray-800 p-4 rounded-lg shadow-md mb-6">
      <h4 class="text-lg font-semibold text-indigo-400 mb-2">Company Details</h4>
      <p class="text-white">Name: {company.name}</p>
      <p class="text-white">Symbol: {company.symbol}</p>
      <p class="text-white">Rank: {company.rank}</p>
      <p class="text-white">Rank Change: {company.rank_change}</p>
      <p class="text-white">Years in Rank: {company.years_in_rank}</p>
    </div>

    <!-- Financial Indicators -->
    <div class="bg-gray-800 p-4 rounded-lg shadow-md">
      <h4 class="text-lg font-semibold text-indigo-400 mb-2">Financial Indicators</h4>
      <ul class="space-y-2">
        <li class="text-white">Revenue: ${financialIndicators.revenue}</li>
        <li class="text-white">Profit: ${financialIndicators.profit}</li>
        <li class="text-white">Assets: ${financialIndicators.assets}</li>
        <li class="text-white">Employees: {financialIndicators.employees}</li>
        <li class="text-white">ROE: {financialIndicators.roe}</li>
        <li class="text-white">P/E Ratio: {financialIndicators.price_to_earnings_ratio}</li>
        <li class="text-white">Stock Volatility: {financialIndicators.stock_volatility}</li>
        <li class="text-white">Dividend Yield: {financialIndicators.dividend_yield}</li>
        <li class="text-white">Earnings per Share: {financialIndicators.earnings_per_share}</li>
        <li class="text-white">EV/EBITDA: {financialIndicators.EV_to_EBITDA}</li>
        <li class="text-white">Profit Change (%): {financialIndicators.profit_change_percentage}</li>
        <li class="text-white">Revenue Change (%): {financialIndicators.revenue_change_percentage}</li>
      </ul>
    </div>
  {:else}
    <p class="text-white">Please select a company to view details.</p>
  {/if}
</div>
