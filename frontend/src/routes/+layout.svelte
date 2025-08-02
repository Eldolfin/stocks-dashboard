
<script>
  import "../app.css";
</script>

<div class="flex flex-col lg:flex-row min-h-screen">
  <!-- Sidebar -->
  <aside class="lg:w-20 w-full flex lg:flex-col flex-row items-center justify-around lg:justify-start lg:space-y-6 py-4 lg:py-6 bg-gradient-to-b from-[#0a0f1c] to-[#141e30] shadow-lg">
    <div class="w-8 h-8 bg-brand rounded-full shadow-inner animate-pulse"></div>
    <a href="/" title="Home" class="hover:scale-110 transition-transform">🏠</a>
    <a href="/portfolio" title="Portfolio" class="hover:scale-110 transition-transform">📊</a>
    <button title="Login" class="hover:scale-110 transition-transform">🔐</button>
  </aside>

  <!-- Main -->
  <main class="flex-1 px-4 sm:px-6 py-6 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a]">
    <slot />
  </main>
</div>
