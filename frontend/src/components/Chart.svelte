<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  // Dynamic results that will be passed to this component
  export let dynamicResults = [];

  let chartInstance;

  const chartData = {
    labels: [],
    datasets: [{
      label: 'Company Scores',
      data: [],
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };

  // Initialize the chart when the component mounts
  onMount(() => {
    const ctx = document.getElementById('rankingChart')?.getContext('2d');
    if (ctx) {
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          scales: {
            x: { beginAtZero: true },
            y: { beginAtZero: true }
          }
        }
      })
    }
  });

  // Watch for changes in dynamicResults and update the chart
  $: dynamicResults, updateChart(dynamicResults);

  function updateChart(data) {
    if (data.length > 0) {
      // Update the labels and dataset with the new data
      chartData.labels = data.map(result => result.name);
      chartData.datasets[0].data = data.map(result => result.score);

      // Update the chart with the new data
      if (chartInstance) {
        chartInstance.update();
      }
    }
  }
</script>

<div>
  <canvas id="rankingChart" width="400" height="200"></canvas>
</div>
