<script>
  import { onMount } from "svelte";
  import CompanySelector from "./components/CompanySelector.svelte";
  import Results from "./components/Results.svelte";

  let selectedCompanies = [];
  let weights = [];
  let results = null;

  const handleSubmit = async () => {
    const response = await fetch('http://localhost:5000/api/analyze/waspas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        companies: selectedCompanies,
        weights: weights
      })
    });

    if (response.ok) {
      const data = await response.json();
      results = data;
    } else {
      alert('Error: ' + response.statusText);
    }
  };
</script>

<main>
  <h1>WASPAS Analysis</h1>

  <!-- Company Selector -->
  <CompanySelector bind:selectedCompanies />

  <div>
    <label for="weights">Enter Weights (comma-separated):</label>
    <input id="weights" type="text" bind:value={weights} />
  </div>

  <button on:click={handleSubmit}>Submit</button>

  <!-- Results -->
  {#if results}
    <Results {results} />
  {/if}
</main>

<style>
  main {
    padding: 20px;
  }
  h1 {
    text-align: center;
  }
  input {
    margin: 10px;
  }
  button {
    margin-top: 10px;
  }
</style>
