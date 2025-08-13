import "jsr:@std/dotenv/load";
import adapterNode from '@sveltejs/adapter-node';
import adapterStatic from '@sveltejs/adapter-static';

import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: Deno.env.get("SVELTE_ADAPTER") === 'static'
			?
			adapterStatic({
				out: 'build-static', precompress: true, fallback: 'index.html'
			})
			:
			adapterNode({
				out: 'build', precompress: false,
			})
	},
	vitePlugin: {
		inspector: true
	}
};

export default config;
