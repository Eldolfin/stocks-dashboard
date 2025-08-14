### Static Build Configuration

The SvelteKit frontend is configured for static site generation using `@sveltejs/adapter-static`. To enable static builds, the following changes were made:

- **Server-side `load` functions moved to client-side:** All data fetching logic previously residing in `+page.server.ts` files for dynamic routes (`details/[ticker]`, `compare/[tickers]`) has been moved to their respective `+page.svelte` components. The `+page.server.ts` files have been removed.
- **Dynamic Path Parameters refactored to Query Parameters:**
  - Routes like `/details/[ticker]` and `/compare/[tickers]` have been refactored. The `[ticker]` and `[tickers]` segments are now passed as query parameters (e.g., `/details?ticker=AAPL`, `/compare?tickers=AAPL,MSFT`).
  - The `src/routes/details/[ticker]` and `src/routes/compare/[tickers]` directories have been renamed to `src/routes/details` and `src/routes/compare` respectively.
  - Similarly, `src/routes/portfolio/analysis/[sheet_name]` has been refactored to `src/routes/portfolio/analysis?sheet_name=...`, and its directory renamed to `src/routes/portfolio/analysis`.
  - All internal links navigating to these routes have been updated to use the new query parameter format.
- **Client-side Authentication in Layout:** The user authentication logic in `src/routes/+layout.svelte` has been made entirely client-side, removing reliance on server-side data fetching for initial rendering.
- **`svelte.config.js` updated for `adapter-static`:** The `adapter-static` configuration now includes a `fallback: 'index.html'` option. This ensures that any route not explicitly prerendered will fall back to `index.html`, allowing client-side routing to take over for dynamic content.

To build the frontend statically, use the command: `just build-static`.
