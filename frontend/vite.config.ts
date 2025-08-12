import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 3000
	},
	build: {
		target: 'esnext',
		assetsInlineLimit: 0,
	},
	base: '', // forces relative paths
});
