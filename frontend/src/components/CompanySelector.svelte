<script>
  import { onMount } from 'svelte';
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';

  let companies = [];

  onMount(async () => {
    const res = await fetch('/api/companies');
    companies = await res.json();
  });

  function moveToSelected(company) {
    selectedCompanies.update(current => [...current, company]);
    companies = companies.filter(c => c !== company)
    console.log(selectedCompanies)
  }

  function moveToPossible(company) {
    companies = [...companies, company];
    selectedCompanies.update(current => current.filter(c => c !== company));
    console.log(selectedCompanies)
  }
</script>

<!-- Content Below Navbar (Centered) -->
<div class="mt-20 flex justify-center items-center h-fit">
  <!-- Your main content goes here -->
  <div class="text-center">
    <h1 class="text-4xl font-bold text-white">Investment decision calculator</h1>
    <p class="text-lg text-gray-400 mt-2">Welcome, investment decision calculator will rank the companies according to one of the for MCDA methods that are available below. You can find the criteria list on separate page. Please choose at least three companies from list below and then choose an MCDA method.</p>
  </div>
</div>

<div class="container flex flex-col md:flex-row gap-8 mt-8">
  <!-- Possible Companies Panel -->
  <div class="panel flex-1 max-w-xl bg-gray-850 p-4 border border-indigo-600 rounded-lg shadow-lg">
    <h3 class="text-xl font-semibold text-white mb-4">Companies</h3>
    <ul class="list-none p-0 m-0 max-h-96 overflow-y-auto">
      {#each companies as company}
        <li class="flex justify-between items-center mb-2">
          <span class="text-white cursor-pointer whitespace-nowrap overflow-hidden"
            on:click={() => moveToSelected(company)}>{company.name} ({company.symbol})</span>
          <button
            class="ml-2 mr-2 narrow-button text-blue-500 hover:text-blue-700"
            on:click={() => moveToSelected(company)}>
            →
          </button>
        </li>
      {/each}
    </ul>
  </div>

  <!-- Selected Companies Panel -->
  <div class="panel flex-1 max-w-xl bg-gray-850 p-4 border border-indigo-600 rounded-lg shadow-lg">
    <h3 class="text-xl font-semibold text-white mb-4">Selected Companies</h3>
    <ul class="list-none p-0 m-0 max-h-96 overflow-y-auto">
      {#each $selectedCompanies as company}
        <li class="flex justify-between items-center mb-2">
          <span class="text-white cursor-pointer whitespace-nowrap overflow-hidden"
            on:click={() => moveToPossible(company)}>{company.name} ({company.symbol})</span>
          <button
            class="ml-2 narrow-button text-blue-500 hover:text-blue-700"
            on:click={() => moveToPossible(company)}>
            ←
          </button>
        </li>
      {/each}
    </ul>
  </div>
</div>

<style>
  .btn-primary {
    @apply bg-blue-500 text-white px-4 py-2 rounded-md font-semibold hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400;
  }

  .btn-secondary {
    @apply bg-gray-600 text-white px-3 py-1 rounded-md hover:bg-gray-500;
  }

  .narrow-button {
    padding: 0.2em 1.0em; /* Reduced vertical padding for lower height buttons */
  }
</style>
