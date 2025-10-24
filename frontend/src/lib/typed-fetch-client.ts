import createClient from 'openapi-fetch';
import type { paths } from '../generated/api';
import { browser } from '$app/environment';

const baseUrlExternal: string = import.meta.env.VITE_API_BASE_EXTERNAL ?? '/';

export const baseUrl = browser ? baseUrlExternal : 'http://backend:5000';

export const client = createClient<paths>({
	baseUrl,
	credentials: 'include'
});
