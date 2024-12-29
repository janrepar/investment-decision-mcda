<script>
  import { onMount } from "svelte";
  let results = null;

  const analyze = async () => {
    const response = await fetch(`/api/analyze/${currentMethod}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        companies: selectedCompanies,
        weights: Object.values(weights),
      }),
    });
    results = await response.json();
  };
</script>

<h3>Results</h3>


{#if results}
  <pre>{JSON.stringify(results, null, 2)}</pre>
{/if}
