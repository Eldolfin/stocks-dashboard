import createClient from 'openapi-fetch';
import type { paths } from '../generated/api';
import { browser } from '$app/environment';

const baseUrlExternal: string = import.meta.env.VITE_API_BASE_EXTERNAL ?? '/';
const baseUrlInternal: string = import.meta.env.VITE_API_BASE_INTERNAL ?? 'http://backend:5000';

export const baseUrl = browser ? baseUrlExternal : baseUrlInternal;

export const client = createClient<paths>({
	baseUrl,
	credentials: 'include'
});
