<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let dynamicResults = [];

  let chartInstance;

  // Data structure for chart
  const chartData = {
    labels: [], // Company names
    datasets: [
      {
        label: 'WASPAS',
        data: [], // WASPAS scores
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'WPM',
        data: [], // WPM scores
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'WSM',
        data: [], // WSM scores
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      }
    ]
  };

  // Initialize chart
  onMount(() => {
    const ctx = document.getElementById('rankingChart').getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true,
        scales: {
          x: {
            beginAtZero: true,
            stacked: true
          },
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          legend: {
            position: 'top',
          },
        },
      }
    });
  });

  // Update chart data when dynamicResults change
  $: dynamicResults, updateChart(dynamicResults);

  function updateChart(data) {
    if (data.length > 0) {
      // Update labels with company names
      chartData.labels = data.map(result => result.name);

      // Update the datasets for each method (WASPAS, WPM, WSM)
      chartData.datasets[0].data = data.map(result => result.waspasScore);
      chartData.datasets[1].data = data.map(result => result.wpmScore);
      chartData.datasets[2].data = data.map(result => result.wsmScore);

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
