<script>
  export let selectedCompanies = [];

  const companies = [
    { id: 1, name: "Walmart" },
    { id: 2, name: "Amazon" },
    { id: 3, name: "Toyota" },
    { id: 4, name: "State Grid" },
    { id: 5, name: "China State Construction Engineering" }
  ];

  const toggleCompany = (companyId) => {
    if (selectedCompanies.includes(companyId)) {
      selectedCompanies = selectedCompanies.filter(id => id !== companyId);
    } else {
      selectedCompanies = [...selectedCompanies, companyId];
    }
  };
</script>

<div>
  <h3>Select Companies</h3>
  {#each companies as company}
    <label>
      <input type="checkbox" value={company.id} bind:group={selectedCompanies} />
      {company.name}
    </label>
  {/each}
</div>
