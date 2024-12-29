<script>
  import Navigation from './components/Navigation.svelte';
  import Tabs from './components/Tabs.svelte';
  import CompanySelector from './components/CompanySelector.svelte';
  import CompanyDetails from './components/CompanyDetails.svelte';
  import Results from "./components/Results.svelte";

  // Get the current page from localStorage or default to 'analysis'
  let currentPage = localStorage.getItem('currentPage') || 'analysis';
  let activeTab = 0;

  function navigate(page = "analysis") {
    currentPage = page;
    // Store the current page in localStorage
    localStorage.setItem('currentPage', page);
  }
</script>

<Navigation {navigate} />

{#if currentPage === 'analysis'}
  <CompanySelector />
  <Tabs />
  <Results />
{/if}

{#if currentPage === 'overview'}
  <p>Company Overview Page</p>
  <CompanyDetails />
{/if}

