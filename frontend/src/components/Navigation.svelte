<script>
  export let navigate;
  let isMenuOpen = false;

  function goToPage(page) {
    navigate(page);
    if (isMenuOpen) {
      isMenuOpen = false; // Close the mobile menu after navigating
    }
  }

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }

  function closeMenu() {
    isMenuOpen = false;
  }
</script>

<!-- Fixed Navbar -->
<nav class="flex items-center justify-between p-4 border-b border-gray-300 bg-gray-800 fixed top-0 left-0 right-0 z-50">
  <!-- Logo -->
  <img src="/path-to-logo.png" alt="Logo" class="h-10 mr-8" />

  <!-- Desktop Nav Buttons -->
  <div class="flex space-x-6 hidden md:flex">
    <button
      class="text-white hover:text-blue-400 transition-colors font-semibold"
      on:click={() => goToPage('analysis')}
    >
      Analysis
    </button>
    <button
      class="text-white hover:text-blue-400 transition-colors font-semibold"
      on:click={() => goToPage('overview')}
    >
      Overview
    </button>
  </div>

  <!-- Mobile Menu Button -->
  <button
    class="md:hidden text-white ml-8"
    on:click={toggleMenu}
  >
    ☰
  </button>

  <!-- Mobile Menu -->
  <div class={`md:hidden fixed inset-0 bg-black bg-opacity-50 ${isMenuOpen ? 'block' : 'hidden'}`} on:click={closeMenu}>
    <div class="flex justify-end p-6">
      <button class="text-white" on:click={closeMenu}>×</button>
    </div>
    <div class="flex flex-col items-center space-y-6">
      <button
        class="text-white hover:text-blue-400 transition-colors"
        on:click={() => goToPage('analysis')}
      >
        Analysis
      </button>
      <button
        class="text-white hover:text-blue-400 transition-colors"
        on:click={() => goToPage('overview')}
      >
        Overview
      </button>
    </div>
  </div>
</nav>

<style>
  button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.8em 1.2em; /* Narrower button size */
    font-size: 1.1em;
    font-weight: 500;
    font-family: inherit;
    background-color: #1a1a1a;
    cursor: pointer;
    transition: border-color 0.25s;
  }

  button:hover {
    border-color: #646cff;
  }

  button:focus {
    outline: 4px auto -webkit-focus-ring-color;
  }
</style>
