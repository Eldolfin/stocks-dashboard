import createClient from 'openapi-fetch';
import type { paths } from '../generated/api';
import { browser, dev } from '$app/environment';

export let baseUrl: string = '';
if (dev && browser) {
	baseUrl = 'http://localhost:5000';
} else if (dev && !browser) {
	baseUrl = "http://backend:5000";
} else if (browser && !dev) {
	baseUrl = '/api';
} else {
	baseUrl = browser ? '/' : 'http://caddy/api';
}

export const client = createClient<paths>({
	baseUrl,
	credentials: 'include'
});
