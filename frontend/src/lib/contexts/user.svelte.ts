import { getContext, setContext } from "svelte";

const key = {};

export interface User {
  loggedIn: boolean;
  profilePicture: string | null;
  logout: () => void;
}
function newUser(): User {
  const user = $state({
    loggedIn: false,
    profilePicture: null,
    logout: () => {
      user.loggedIn = false;
      user.profilePicture = null;
    },
  });
  return user;
}

export function setUserContext() {
  const user = newUser();
  setContext(key, user);
  return user;
}

export function getUserContext() {
  return getContext(key) as User;
}
