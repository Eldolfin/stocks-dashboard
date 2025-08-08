import type { Load } from '@sveltejs/kit';
import { client } from '$lib/typed-fetch-client';

export const load: Load = async ({ depends, fetch }) => {
	depends('data:user_auth');
	let isLoggedIn = false;
	let userProfilePicture: string | null = null;
	let error: string = '';

	const baseUrl = '';

	try {
		const { data, error: err } = await client.GET('/api/user', { fetch });
		if (data) {
			userProfilePicture = data.profile_picture
				? `${baseUrl}/api/profile/pictures/${data.profile_picture}`
				: null;
			isLoggedIn = true;
		} else if (err) {
			// not logged in
		}
	} catch (e) {
		console.error('Failed to fetch user profile:', e);
		error = String(e);
	}

	return {
		isLoggedIn,
		userProfilePicture,
		error
	};
};
