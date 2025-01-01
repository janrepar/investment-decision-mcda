<script>
  import { selectedCompanies } from '../stores/selectedCompaniesStore.js';
  import AhpResults from "../components/AhpResults.svelte";
  import Chart from "../components/Chart.svelte";
  import { onMount } from "svelte";

  let weightDerivation = "geometric";
  let results = null;
  let criteria = []; // Store the criteria to be sent to the backend
  let pairwiseMatrix = []; // Store the pairwise matrix entered by the user
  let isModalOpen = false; // Track the state of the popup modal

  // Store for dynamic results
  let dynamicResults = [];

  // Valid values for pairwise comparisons, including reciprocals
  const validValues = [1, 3, 1/3, 5, 1/5, 7, 9, 1/7, 1/9];

  // Fetch criteria on mount
  onMount(async () => {
    const response = await fetch('/api/criteria');
    criteria = await response.json();
    // Initialize pairwise matrix: 1 on the diagonal, null for other cells
    pairwiseMatrix = criteria.map((_, i) => criteria.map((_, j) => (i === j ? 1 : 1)));
  });

  // Function to validate and update pairwise matrix
  // Function to find the closest valid value
  const getClosestValidValue = (inputValue) => {
    return validValues.reduce((prev, curr) => {
      return Math.abs(curr - inputValue) < Math.abs(prev - inputValue) ? curr : prev;
    });
  };

  // Function to update the matrix
  const updateMatrix = (i, j, value) => {
    // Check if the value is valid
    if (validValues.includes(value)) {
      pairwiseMatrix[i][j] = value;
      pairwiseMatrix[j][i] = value ? 1 / value : null; // Update reciprocal
    } else {
      // If the value is not valid, find the closest valid value
      const closestValidValue = getClosestValidValue(value);
      pairwiseMatrix[i][j] = closestValidValue;
      pairwiseMatrix[j][i] = closestValidValue ? 1 / closestValidValue : null; // Update reciprocal
    }
  };

  // Analyze AHP method
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
        pairwise_matrix: pairwiseMatrix, // Send the pairwise matrix entered by the user
      }),
    });

    results = await response.json();

    if (!response.ok) {
      // If the backend returns a consistency error
      if (results.error) {
        alert(results.error); // Display the error message as an alert
      }
      return;
    }

    // Update the dynamicResults after getting the results
    dynamicResults = results.aggregated_scores.map((company) => ({
      name: company.name,
      score: company.score
    }));
  };

  // Function to toggle popup modal
  const toggleModal = () => {
    isModalOpen = !isModalOpen;
  };
</script>

<div class="max-w-xl mx-auto bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600">
  <h3 class="text-2xl font-semibold text-white mb-4">AHP Method</h3>

  <!-- Weight Derivation Selection -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-300 mb-2">
      Weight Derivation:
    </label>
    <select
      id="weight-derivation"
      bind:value={weightDerivation}
      class="w-full px-3 py-2 bg-gray-800 text-white border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:outline-none"
    >
      <option value="geometric" title="Uses geometric mean of pairwise comparison values.">
        Geometric
      </option>
      <option value="mean" title="Averages the pairwise comparison values.">
        Mean
      </option>
      <option value="max_eigen" title="Derives weights from the largest eigenvalue of the pairwise comparison matrix.">
        Max Eigen
      </option>
    </select>
  </div>

  <!-- Button to show Pairwise Matrix in Popup -->
  <button
    on:click={toggleModal}
    class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 mb-4"
  >
    Set Criteria Pairwise Comparison Matrix
  </button>

  <!-- Modal for Pairwise Matrix -->
  {#if isModalOpen}
    <div class="fixed inset-0 bg-gray-800 bg-opacity-95 flex justify-center items-center z-50">
      <div class="bg-gray-850 p-6 rounded-lg shadow-md border border-indigo-600 max-w-[98vw] max-h-[98vh]  overflow-auto">
        <h4 class="text-lg font-semibold text-indigo-400 mb-4">Pairwise Comparison Matrix</h4>
        <table class="min-w-full bg-gray-800 rounded-lg shadow-md border border-gray-700">
          <thead class="top-0 bg-gray-850 z-10">
            <tr>
              <th class="text-center py-2 px-4 text-gray-300">Criterion</th>
              {#each criteria as criterion}
                <th class="text-left py-2 px-4 text-gray-300">{criterion.name}</th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each pairwiseMatrix as row, i}
              <tr class="border-b border-gray-700">
                <td class="py-2 px-4 text-white">{criteria[i].name}</td> <!-- Row names (Criteria) -->
                {#each row as cell, j}
                  <td class="py-2 px-4">
                    <input
                      type="number"
                      class="border p-2 rounded text-white w-full bg-gray-800"
                      bind:value={pairwiseMatrix[i][j]}
                      on:input={(e) => updateMatrix(i, j, parseFloat(e.target.value))}
                      placeholder={i === j ? '1' : 'Enter value'}
                      disabled={i === j}
                      min="0" max="9" step="3"
                    />
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>

        <!-- Close Button for Modal -->
        <button
          on:click={toggleModal}
          class="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
        >
          Close
        </button>
      </div>
    </div>
  {/if}

  <!-- Analyze Button -->
  <button
    on:click={analyzeAHP}
    class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
  >
    Analyze
  </button>

  <!-- Results Component -->
  <AhpResults {results} />

  <!-- Chart Component -->
  <div class="mt-6">
    <Chart {dynamicResults} />
  </div>
</div>
