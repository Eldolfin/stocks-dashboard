import { client } from "$lib/typed-fetch-client";

export const load = async ({depends, fetch }) => {
  depends("data:user_auth");
  let isLoggedIn = false;
  let userProfilePicture = null;
  let error = '';
  try {
    const response = await client.GET('/api/user', {fetch});
    if (response.data) {
      userProfilePicture = response.data.profile_picture ? `${baseUrl}/api/profile/pictures/${response.data.profile_picture}` : null;
      isLoggedIn = true;
      error = response.error;
    } else if (response.error) {
      // not logged in
    }
  } catch (e) {
    console.error('Failed to fetch user profile:', e);
      error = String(e);
  }
  return {
    isLoggedIn, userProfilePicture
  }
}
