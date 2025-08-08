import createClient from 'openapi-fetch';
import type { paths } from '../generated/api';
import { browser } from '$app/environment';

export const baseUrl = browser ? '/' : 'http://backend:5000';

export const client = createClient<paths>({
	baseUrl,
	credentials: 'include'
});
