<script>
  export let results;
</script>

<h3>Results</h3>

<h4>WSM Result</h4>
<ul>
  {#each results.WSM_result as { company_name, score }}
    <li>{company_name}: {score}</li>
  {/each}
</ul>

<h4>WPM Result</h4>
<ul>
  {#each results.WPM_result as { company_name, score }}
    <li>{company_name}: {score}</li>
  {/each}
</ul>

<h4>WASPAS Result</h4>
<ul>
  {#each results.WASPAS_result as { company_name, score }}
    <li>{company_name}: {score}</li>
  {/each}
</ul>
